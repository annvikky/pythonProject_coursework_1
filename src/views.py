import json
import os

import pandas as pd

from src.utils import (filter_info_by_card, filter_info_by_date,  # read_transactions_from_excel_file,
                       get_currency_rates, get_greeting, get_stock_prices, get_top_transactions)

settings = json.loads(
    open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_settings.json"),
        "r",
    ).read()
)


def main_page_with_json_answer(df: pd.DataFrame, date: str):  # user_settings
    """Функция для вывода информации с фильтрацией по дате."""

    filtered_transactions = filter_info_by_date(date, df)
    currency_list = settings["currency_list"]
    stock_list = settings["stock_list"]

    data_for_user = {
        "greeting": get_greeting(),
        "cards": filter_info_by_card(filtered_transactions),
        "top_transactions": get_top_transactions(filtered_transactions),
        "currency_rates": get_currency_rates(currency_list),
        "stock_prices": get_stock_prices(stock_list),
    }
    json_answer = json.dumps(data_for_user, indent=4, ensure_ascii=False)
    return json_answer


# print(main_page_with_json_answer(read_transactions_from_excel_file(), '20.02.2021 00:00:00'))
