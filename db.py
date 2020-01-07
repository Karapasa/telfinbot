import os
import sqlite3

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()


def _init_db() -> None:
    """Инициализирует БД"""
    with open("creatdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expenses'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
