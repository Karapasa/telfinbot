create table budget(
    cat_code varchar(255) primary key,
    limits integer
);

create table category(
    cat_code varchar(255) primary key,
    name varchar(255),
    aliases text
);

create table expenses(
    id integer primary key autoincrement,
    amount integer,
    dateexp date,
    category_name varchar(255),
    raw_text text,
    FOREIGN KEY(category_name) REFERENCES category(cat_code)
    FOREIGN KEY(category_name) REFERENCES budget(cat_code)
);

insert into category (cat_code, name, aliases)
values
    ("products", "еда", "продукты"),
    ("transport", "транспорт", ""),
    ("dinner", "обеды", "столовая, ланч, перекус, бизнес ланч"),
    ("connection", "связь", "телефон, интернет, сервисы"),
    ("medicine", "лекарства", ""),
    ("house", "жилье", "коммуналка"),
    ("clothes", "одежда", "ламода"),
    ("sport", "спорт", "зал, спортодежда, тренер"),
    ("vacation", "отпуск", ""),
    ("holiday", "отдых", ""),
    ("subscriptions", "подписки","яндекс, гугл"),
    ("purchases", "покупки", ""),
    ("other", "прочее", "прочие");

insert into budget (cat_code, limits) values ('other', 15000);
insert into expenses (amount, category_name, raw_text) values (0, 'other', 'тестовый расход');
