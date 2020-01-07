from datetime import datetime
from typing import Optional

import pytz

from db import cursor, conn

lss = dict(enumerate([x[0] for x in cursor.execute("SELECT name FROM category").fetchall()], start=1))


def execut(amount: int, cat_name: str, raw_text: str = '') -> Optional[str]:
    # Добавляет новый расход
    try:
        cat_code = cursor.execute(f"SELECT cat_code FROM category WHERE name = '{cat_name}';").fetchone()[0]
        cursor.execute(
            f"INSERT INTO expenses (amount, dateexp, category_name, raw_text) "
            f"VALUES ({amount},'{_get_now_datetime()}', '{cat_code}', '{raw_text}');")
        conn.commit()
    except:
        return "Нет такой категории"


# TODO сделать рефакторинг, очень плохо смотрится код
def add_expense(insert: list) -> None:
    # Определяет данные для добавления расхода
    if len(insert) == 2:
        execut(int(insert[0]), insert[1])
    elif len(insert) == 3:
        execut(int(insert[0]), insert[1], insert[2])


def last_5(cat_now) -> str:
    # Показать последние 5 расходов в категории с функции удалить
    last_exp = cursor.execute(f"SELECT e.id, e.amount, c.name, e.raw_text FROM expenses e"
                              f" LEFT JOIN category c ON e.category_name = c.cat_code"
                              f" WHERE c.name = '{cat_now}'"
                              f" ORDER BY e.dateexp DESC LIMIT 5;").fetchall()
    last_expenses = []
    for exp in last_exp:
        last_expenses.append({'id': exp[0],
                              'amount': exp[1],
                              'category': exp[2],
                              'comment': exp[3]})

    last_expenses_rows = [
        f"{row['amount']} руб. на {row['category']} {'('+row['comment']+')' if row['comment'] !='' else ''} —  нажми "
        f"/del{row['id']} для удаления"
        for row in last_expenses]
    answer_message = "Последние сохранённые траты:\n* " + "\n* ".join(last_expenses_rows)
    return answer_message


def delete(row_id: int) -> None:
    # Удаляет расход по id
    row_id = int(row_id)
    cursor.execute(f"delete from expenses where id={row_id}")
    conn.commit()

def get_mounth_stat() -> str:
    row_stat = cursor.execute("SELECT c.name, sum(e.amount) FROM expenses e"
                              " LEFT JOIN category c ON e.category_name = c.cat_code"
                              " GROUP BY c.name").fetchall()
    answer_with_stat = []
    for row in row_stat:
        answer_with_stat.append(f'Категория: "{row[0]}" - общие расходы: {row[1]} руб.')
    answer_stat = "Траты за месяц составили:\n*" + '\n*'.join(answer_with_stat)
    return answer_stat


def _get_now_datetime() -> str:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz).strftime("%Y-%m-%d")
    return now
