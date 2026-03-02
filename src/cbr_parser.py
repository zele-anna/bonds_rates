import io

import pandas as pd
import requests


def get_key_rate(date_from, date_to):
    """Загрузка данных по ключевой ставке через веб-форму ЦБ. Формат дат: ДД.ММ.ГГГГ."""
    url = "https://www.cbr.ru/hd_base/KeyRate/"
    params = {"UniDbQuery.Posted": "True", "UniDbQuery.From": date_from, "UniDbQuery.To": date_to}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.cbr.ru",
    }

    try:
        # Получаем HTML-страницу
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = pd.read_html(io.StringIO(response.text))

        # Создаем таблицу с данными
        df = data[0]
        df.columns = ["Дата", "Ключевая ставка"]

        # Конвертируем дату
        df["Дата"] = pd.to_datetime(df["Дата"], dayfirst=True)

        # Считаем количество записей
        rows_count = df.shape[0]
        print(f"Всего строк данных по ключевой ставке: {rows_count}")

        return df.sort_values("Дата").reset_index(drop=True)

    except Exception as e:
        return f"Ошибка: {e}"


def get_cbr_zcyc_params(date_from, date_to):
    """Загрузка данных КБД (G-кривой) с сайта ЦБ РФ."""

    url = "https://www.cbr.ru/hd_base/zcyc_params/"

    # Параметры из вашей ссылки
    params = {"UniDbQuery.Posted": "True", "UniDbQuery.From": date_from, "UniDbQuery.To": date_to}

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        response.raise_for_status()

        # Читаем все таблицы со страницы
        tables = pd.read_html(io.StringIO(response.text), decimal=",", thousands="\xa0")

        if not tables:
            return "Таблицы не найдены"

        df = tables[0]  # Берем первую таблицу

        # Находим колонку с датой и конвертируем ее
        date_col = df.columns[0]
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True)

        # Считаем количество записей
        rows_count = df.shape[0]
        print(f"Всего строк данных по кривой доходности: {rows_count}")

        return df.sort_values(date_col).reset_index(drop=True)

    except Exception as e:
        return f"Ошибка: {e}"


if __name__ == "__main__":
    pass
