import json
import sqlite3

import pandas as pd


def save_data_to_db(data, db_name: str, table_name: str) -> None:
    """Функция сохранения данных в базу данных."""
    # Создаем подключение к базе данных
    conn = sqlite3.connect(f"{db_name}.db")

    # Записываем данные в таблицу
    # if_exists='replace' перезапишет таблицу, если она уже есть
    # index=False не сохраняет порядковый номер строк pandas как отдельную колонку
    data.to_sql(table_name, conn, if_exists="replace", index=False)

    # Закрываем соединение
    conn.close()
    print(f"Данные успешно сохранены в {db_name}.db, таблица {table_name}")


def get_all_data_from_db_table(table_name: str, db_name: str = "bonds_data.db") -> list:
    """Функция выгрузки всех данных из заданной таблицы БД."""
    conn = sqlite3.connect(db_name)

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql_query(query, conn)

    conn.close()

    json_data = df.to_json(orient="records", force_ascii=False, date_format="iso")

    return json.loads(json_data)


def get_filtered_data_from_db_table(
    filter_by: str, column: str, table_name: str, db_name: str = "bonds_data.db"
) -> list:
    """Функция выгрузки данных из заданной таблицы БД с фильтрацией по заданной колонке."""
    conn = sqlite3.connect(db_name)

    query = f"SELECT * FROM {table_name} WHERE {column} = ?"
    params = [
        filter_by,
    ]

    df = pd.read_sql_query(query, conn, params=params)

    conn.close()

    json_data = df.to_json(orient="records", force_ascii=False, date_format="iso")

    return json.loads(json_data)


if __name__ == "__main__":
    pass
