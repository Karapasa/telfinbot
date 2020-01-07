import os
import emojis
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import server

logging.basicConfig(level=logging.INFO)

TEL_API_TOKEN = os.getenv('TEL_API_TOKEN')
TEL_PROXY = os.getenv('TEL_PROXY_URL')
bot = Bot(token=TEL_API_TOKEN, proxy=TEL_PROXY)
dp = Dispatcher(bot)

switch_cat = ''


def auth(func):
    async def wrapper(message):
        if message['from']['id'] != 735996175:
            return await message.reply('Доступ запрещен', reply=False)
        return await func(message)

    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def process_start_command(message: types.Message):
    await message.answer("FinBot готов к работе:", reply_markup=inline_kb_full)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    server.delete(row_id)
    answer_message = "Удалено"
    await message.answer(answer_message)


# @dp.message_handler(commands=['1'])
# @auth
# async def process_start_command(message: types.Message):
#     await bot.send_message(message.from_user.id, message)


def parse_msg(text: str) -> str:
    #  добавляет расход и парсит текст сообщения либо полное, либо короткое из категории
    list_data = text.split()
    if len(list_data) > 1:
        server.add_expense(list_data)
        answer = f'Новый расход: {list_data[0]}руб. - \"{list_data[1]}\"'
        return answer
    else:
        list_data.append(switch_cat)
        server.add_expense(list_data)
        answer = f'Новый расход: {list_data[0]}руб. - \"{switch_cat}\"'
        return answer


@dp.message_handler()
@auth
async def full_message(msg: types.Message):
    answer = parse_msg(msg.text)
    await msg.answer(text=answer)


# Первая кнопка "расходы"
@dp.callback_query_handler(lambda c: c.data == 'btn1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию:', reply_markup=inline_kb_cat)


# Вторая кнопка "отчет"
@dp.callback_query_handler(lambda c: c.data == 'btn2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Раздел "Отчет":\n' + server.get_mounth_stat())


# Третья кнопка "бюджет"
@dp.callback_query_handler(lambda c: c.data == 'btn3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Бюджет в разработке!')


# Главное меню
main_btn_1 = InlineKeyboardButton(emojis.encode(':memo:') + ' Расходы', callback_data='btn1')
main_btn_2 = InlineKeyboardButton(emojis.encode(':chart_with_upwards_trend:') + ' Отчет', callback_data='btn2')
main_btn_3 = InlineKeyboardButton(emojis.encode(':moneybag:') + ' Бюджет', callback_data='btn3')

# Клавиатура главного меню
inline_kb_full = InlineKeyboardMarkup()
inline_kb_full.row(main_btn_1, main_btn_2, main_btn_3)


# TODO сделать регулярку для вытаскивания номера кнопки
# Ответы на кнопки категорий
@dp.callback_query_handler(lambda c: c.data.startswith('cat_btn'))
async def process_callback_cat_buttons(callback_query: types.CallbackQuery):
    global switch_cat
    switch_cat = server.lss[int(callback_query.data[-1])]
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=f'{server.last_5(switch_cat)} \n\nВведите сумму на {switch_cat}:')


# Каталог категорий
cat_btn_1 = InlineKeyboardButton(emojis.encode(':bread:') + ' Еда', callback_data='cat_btn1')
cat_btn_2 = InlineKeyboardButton(emojis.encode(':bus:') + ' Транспорт', callback_data='cat_btn2')
cat_btn_3 = InlineKeyboardButton(emojis.encode(':iphone:') + ' Связь', callback_data='cat_btn4')
cat_btn_4 = InlineKeyboardButton(emojis.encode(':sandwich:') + ' Обеды', callback_data='cat_btn3')
cat_btn_5 = InlineKeyboardButton(emojis.encode(':thermometer:') + ' Лекарства', callback_data='cat_btn5')
cat_btn_6 = InlineKeyboardButton(emojis.encode(':house:') + ' Жилье', callback_data='cat_btn6')
cat_btn_7 = InlineKeyboardButton(emojis.encode(':open_file_folder:') + ' Прочие', callback_data='cat_btn12')
cat_btn_8 = InlineKeyboardButton(emojis.encode(':beers:') + ' Отдых', callback_data='cat_btn10')
cat_btn_9 = InlineKeyboardButton(emojis.encode(':tshirt:') + ' Одежда', callback_data='cat_btn7')
cat_btn_10 = InlineKeyboardButton(emojis.encode(':boxing_glove:') + ' Спорт', callback_data='cat_btn8')
cat_btn_11 = InlineKeyboardButton(emojis.encode(':beach_umbrella:') + ' Отпуск', callback_data='cat_btn9')
cat_btn_12 = InlineKeyboardButton(emojis.encode(':money_with_wings:') + ' Покупки', callback_data='cat_btn11')
cat_btn_13 = InlineKeyboardButton(emojis.encode(':pushpin:') + ' Подписки', callback_data='cat_btn13')

# Клавиатура для категорий
inline_kb_cat = InlineKeyboardMarkup(row_width=3)
inline_kb_cat.add(cat_btn_1, cat_btn_2, cat_btn_3, cat_btn_4, cat_btn_5, cat_btn_6, cat_btn_7, cat_btn_8, cat_btn_9,
                  cat_btn_10, cat_btn_11, cat_btn_12, cat_btn_13)

if __name__ == '__main__':
    executor.start_polling(dp)
