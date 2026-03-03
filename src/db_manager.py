import json
import sqlite3

import pandas as pd


def save_data_to_db(df, table_name: str, db_name: str = "bonds_data") -> None:
    """Функция сохранения данных в базу данных."""
    # Создаем подключение к базе данных
    conn = sqlite3.connect(f"{db_name}.db")

    # Записываем данные в таблицу
    # if_exists='replace' перезапишет таблицу, если она уже есть
    # index=False не сохраняет порядковый номер строк pandas как отдельную колонку
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Закрываем соединение
    conn.close()
    print(f"Данные успешно сохранены в {db_name}.db, таблица {table_name}")


def normalize_bonds_table(db_name: str = "bonds_data.db"):
    """Функция для присвоения полю SECID значения первичного ключа и изменения типов данных."""
    # Подключаемся к вашей базе
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создаем новую таблицу с нужными типами
    cursor.execute("""
        CREATE TABLE bonds_new (
            SECID VARCHAR(12) PRIMARY KEY,
            BOARDID VARCHAR(10),
            SHORTNAME TEXT,
            COUPONVALUE REAL,
            NEXTCOUPON TEXT,
            ACCRUEDINT REAL,
            FACEVALUE REAL,
            MATDATE TEXT,
            COUPONPERIOD INTEGER,
            FACEUNIT TEXT,
            ISIN TEXT,
            REGNUMBER TEXT,
            CURRENCYID TEXT,
            COUPONPERCENT REAL,
            CALLOPTIONDATE TEXT,
            PUTOPTIONDATE TEXT,
            BONDTYPE TEXT,
            BONDSUBTYPE TEXT
        )
    """)

    # Переносим данные из старой таблицы в новую
    cursor.execute("""
        INSERT INTO bonds_new
        SELECT * FROM bonds
    """)

    # Удаляем старую таблицу
    cursor.execute("DROP TABLE bonds")

    # Переименовываем новую таблицу в оригинальное название
    cursor.execute("ALTER TABLE bonds_new RENAME TO bonds")

    conn.commit()
    conn.close()

    print("Таблица bonds нормализирована.")


def normalize_trading_data_table(db_name: str = "bonds_data.db"):
    """Функция для привязки таблицы по полю SECID к таблице bonds и изменения типов данных."""
    # Подключаемся к вашей базе
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создаем новую таблицу с нужными типами
    cursor.execute("""
                CREATE TABLE "trading_data_new" (
                    "TRADEDATE" TEXT,
                    "SHORTNAME" TEXT,
                    "SECID" VARCHAR(12),
                    "NUMTRADES" INTEGER,
                    "VALUE" REAL,
                    "LOW" REAL,
                    "HIGH" REAL,
                    "CLOSE" REAL,
                    "LEGALCLOSEPRICE" REAL,
                    "ACCINT" REAL,
                    "WAPRICE" REAL,
                    "YIELDCLOSE" REAL,
                    "OPEN" REAL,
                    "VOLUME" INTEGER,
                    "MARKETPRICE2" REAL,
                    "MARKETPRICE3" REAL,
                    "ADMITTEDQUOTE" TEXT,
                    "MP2VALTRD" REAL,
                    "MARKETPRICE3TRADESVALUE" REAL,
                    "ADMITTEDVALUE" TEXT,
                    "MATDATE" TEXT,
                    "DURATION" REAL,
                    "YIELDATWAP" REAL,
                    "IRICPICLOSE" TEXT,
                    "BEICLOSE" TEXT,
                    "COUPONPERCENT" REAL,
                    "COUPONVALUE" REAL,
                    "FACEVALUE" INTEGER,
                    "CURRENCYID" TEXT,
                    FOREIGN KEY ("SECID") REFERENCES bonds("SECID")
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                );
            """)

    # Переносим данные из старой таблицы в новую
    cursor.execute("""
        INSERT INTO trading_data_new
        SELECT * FROM trading_data
    """)

    # Удаляем старую таблицу
    cursor.execute("DROP TABLE trading_data")

    # Переименовываем новую таблицу в оригинальное название
    cursor.execute("ALTER TABLE trading_data_new RENAME TO trading_data")

    # Создаем индекс по полям SECID и TRADEDATE для ускорения работы
    cursor.execute("CREATE INDEX idx_trading_secid_date ON trading_data (SECID, TRADEDATE);")

    conn.commit()
    conn.close()

    print("Таблица trading_data нормализирована.")


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
