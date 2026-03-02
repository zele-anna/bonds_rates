import sqlite3


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
