import math
from datetime import datetime

import pandas as pd
import requests


def get_bonds_by_matdate(start_date: str = "2026-01-01", end_date: str = "2026-12-31"):
    """Функция для получения списка облигаций со сроком погашения в заданном диапазоне."""

    # URL для получения данных по облигациям
    url = "https://iss.moex.com/iss/engines/stock/markets/bonds/securities.json"

    # Параметр iss.only=securities ограничивает ответ только данными об облигациях
    params = {
        "iss.meta": "off",
        "iss.only": "securities",
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Извлекаем данные
    columns = data["securities"]["columns"]
    rows = data["securities"]["data"]

    # Создаем таблицу, фильтруем по дате до погашения (start_date <= MATDATE <= end_date)
    df = pd.DataFrame(rows, columns=columns)
    filtered_df = df[df["MATDATE"].between(start_date, end_date)]

    # Фильтруем только нужные столбцы
    cols_to_keep = [
        "SECID",
        "BOARDID",
        "SHORTNAME",
        "COUPONVALUE",
        "NEXTCOUPON",
        "ACCRUEDINT",
        "FACEVALUE",
        "MATDATE",
        "COUPONPERIOD",
        "FACEUNIT",
        "ISIN",
        "REGNUMBER",
        "COUPONPERCENT",
        "CALLOPTIONDATE",
        "PUTOPTIONDATE",
        "BONDTYPE",
        "BONDSUBTYPE",
    ]
    filtered_df = filtered_df[cols_to_keep]

    # Считаем количество записей
    rows_count = filtered_df.shape[0]
    print(f"Всего облигаций: {rows_count}")

    return filtered_df


def get_trading_data(bond, period_start, period_end):
    """Функция для получения данных о торгах по выбранным облигациям."""

    # URL для получения данных по облигациям (ISIN, даты до погашения)
    url = "https://iss.moex.com//iss/history/engines/stock/markets/bonds/securities/"

    # В целях оптимизации объема данных установлен фильтр по минимальному количеству сделок за день "numtrades" = 1
    params = {
        "iss.meta": "off",
        "sort_order": "acs",
        "from": period_start,
        "till": period_end,
        "limit": 100,
        "start": 0,
        "numtrades": 1,
        "tradingsession": "3",
        "history.columns": "TRADEDATE,SHORTNAME,SECID,NUMTRADES,VALUE,LOW,HIGH,CLOSE,LEGALCLOSEPRICE,ACCINT,WAPRICE,YIELDCLOSE,OPEN,VOLUME,MARKETPRICE2,MARKETPRICE3,ADMITTEDQUOTE,MP2VALTRD,MARKETPRICE3TRADESVALUE,ADMITTEDVALUE,MATDATE,DURATION,YIELDATWAP,IRICPICLOSE,BEICLOSE,COUPONPERCENT,COUPONVALUE,FACEVALUE,CURRENCYID",
    }

    all_data = []

    while True:
        response = requests.get(f"{url}{bond}.json", params=params)
        response.raise_for_status()
        raw_data = response.json()

        # Данные лежат в ['history']['data']
        rows = raw_data['history']['data']

        if not rows:  # Если данных больше нет — выходим
            break

        all_data.extend(rows)

        # Если строк меньше 100, значит это была последняя страница
        if len(rows) < 100:
            break

        # Увеличиваем смещение для следующей "страницы"
        params["start"] += 100

    # Сразу собираем в удобный DataFrame
    columns = raw_data['history']['columns']

    # Создаем Dataframe
    trading_data_df = pd.DataFrame(all_data, columns=columns)

    return trading_data_df


if __name__ == '__main__':
    pass
