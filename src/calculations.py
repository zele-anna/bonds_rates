import numpy as np


def calculate_bond_var(data: list, confidence_level: float = 0.95) -> tuple:
    """
    Рассчитывает исторический VaR для облигации.
    :param data: список словарей с торговыми данными (JSON)
    :param confidence_level: уровень доверия (0.95 или 0.99)
    :return: кортеж (дневной VaR в %, доходности)
    """
    dirty_prices = []

    # Расчет грязных цен
    for entry in data:
        # Номинал (FACEVALUE), цена в % (CLOSE) и НКД (ACCINT)
        face_value = float(entry["FACEVALUE"])
        clean_price_pct = float(entry["CLOSE"])
        if entry["ACCINT"]:
            accrued_int = float(entry["ACCINT"])
        else:
            accrued_int = 0

        dirty_price = (clean_price_pct / 100) * face_value + accrued_int
        dirty_prices.append(dirty_price)

    # Расчет логарифмических доходностей
    log_returns = []
    for i in range(1, len(dirty_prices)):
        # r = ln(P_t / P_{t-1})
        ret = np.log(dirty_prices[i] / dirty_prices[i - 1])
        log_returns.append(ret)

    # Расчет VaR историческим методом
    alpha = 1 - confidence_level
    var_percent = np.percentile(log_returns, alpha * 100)

    return var_percent, log_returns


if __name__ == "__main__":
    pass
