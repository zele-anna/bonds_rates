import pandas as pd

from cbr_parser import get_cbr_zcyc_params, get_key_rate
from db_manager import save_data_to_db
from moex_parser import get_bonds_by_matdate, get_trading_data

# Получаем данные по облигациям с отбором по интервалу дат погашения
start_mat_date = "2026-10-01"
end_mat_date = "2026-12-31"
bonds_data = get_bonds_by_matdate(start_date=start_mat_date, end_date=end_mat_date)

# Сохраняем данные по облигациям в таблицу bonds БД bonds_data
save_data_to_db(bonds_data, "bonds_data", "bonds")

# Получаем список тикеров выбранных облигаций
tickers_list = bonds_data["SECID"].values.tolist()

# Определяем период запроса торговых данных и отправляем запросы
# Формат дат ГГГГ-ММ-ДД
period_start = "2024-01-01"
period_end = "2025-12-31"
trading_data_df = pd.DataFrame()
for bond in tickers_list:
    df_to_add = get_trading_data(bond, period_start, period_end)
    trading_data_df = pd.concat([trading_data_df, df_to_add], ignore_index=True)

# Считаем количество записей торговых данных
rows_count = trading_data_df.shape[0]
print(f"Всего строк торговых данных по : {rows_count}")

# Сохраняем данные по облигациям в таблицу trading_data БД bonds_data
save_data_to_db(trading_data_df, "bonds_data", "trading_data")

# Определяем период для загрузки данных по ключевой ставке и загружаем данные из ЦБ
# Формат дат ДД.ММ.ГГГГ
key_rate_start_date = "01.01.2024"
key_rate_end_date = "31.12.2025"
df_rates = get_key_rate(key_rate_start_date, key_rate_end_date)

# Определяем период для загрузки данных по кривой доходности и загружаем данные из ЦБ
# Формат дат ДД.ММ.ГГГГ
yc_date_from = '01.01.2024'
yc_date_to = '31.12.2025'
df_yc = get_cbr_zcyc_params(yc_date_from, yc_date_to)

# Избавляемся от мульти-индекса в колонках
df_yc.columns = [str(col[1]) if isinstance(col, tuple) else str(col) for col in df_yc.columns]
if 'Дата' not in df_yc.columns:
    df_yc = df_yc.reset_index()

df_yc = df_yc.rename(columns={'date': 'Дата', 'index': 'Дата'})

# Объединяем данные по ключевой ставке и кривой доходности в один DataFrame
macro_df = pd.merge(df_rates, df_yc, on='Дата', how='inner')

# Сохраняем данные по ключевой ставке и кривой доходности в таблицу macro_data БД bonds_data
save_data_to_db(macro_df, "bonds_data", "macro_data")
