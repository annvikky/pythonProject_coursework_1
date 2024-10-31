from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import (filter_info_by_card, filter_info_by_date, get_currency_rates, get_greeting, get_stock_prices,
                       get_top_transactions, read_transactions_from_excel_file)


@patch("pandas.read_excel")
def test_read_transactions_from_excel_file(mock_read_excel):
    """Тест на чтение файла и возврат транзакций."""
    dataframe = pd.DataFrame({"foo_id": [1, 2, 3]})
    mock_read_excel.return_value = dataframe
    result = read_transactions_from_excel_file()
    mock_read_excel.assert_called_once()
    pd.testing.assert_frame_equal(result, dataframe)


@patch("src.utils.datetime")
@pytest.mark.parametrize(
    "current_hour, expected_greeting",
    [
        (9, "Доброе утро!"),
        (14, "Добрый день!"),
        (20, "Добрый вечер!"),
        (1, "Доброй ночи!"),
    ],
)
def test_get_greeting(
    mock_datetime: MagicMock, current_hour, expected_greeting: str
) -> None:
    """Тест на получение приветствия."""
    mock_time_now = datetime(2024, 9, 1, current_hour, 0, 0)
    mock_datetime.now.return_value = mock_time_now
    result = get_greeting()
    assert result == expected_greeting


def test_filter_info_by_date(transaction_by_date, transaction_by_date_filtered):
    """Тест на корректность работы функции."""
    result = filter_info_by_date("20.02.2021 00:00:00", transaction_by_date)
    assert len(result) == len(transaction_by_date_filtered)


def test_filtered_info_by_different_card(transaction_by_card_1):
    """Тест на корректность работы функции."""
    assert filter_info_by_card(transaction_by_card_1) == [
        {"cashback": 462.07, "last_digits": "1112", "total_spent": -46207.08},
        {"cashback": 5339.49, "last_digits": "4556", "total_spent": 533948.75},
    ]


def test_filtered_info_by_one_card(transaction_by_card_2):
    """Тест на корректность работы функции."""
    assert filter_info_by_card(transaction_by_card_2) == [
        {"cashback": 4877.42, "last_digits": "1112", "total_spent": 487741.67}
    ]


def test_get_top_transactions(top_transaction):
    """Тест на корректность работы функции."""
    assert get_top_transactions(top_transaction) == [
        {
            "amount": -85000.0,
            "category": "Переводы",
            "date": "10.02.2021",
            "description": "Николай Н.",
        },
        {
            "amount": -4800.0,
            "category": "Связь",
            "date": "16.02.2021",
            "description": "Sknt.Ru",
        },
        {
            "amount": -812.3,
            "category": "Аптеки",
            "date": "13.02.2021",
            "description": "Аптека Вита",
        },
        {
            "amount": -700.0,
            "category": "Транспорт",
            "date": "04.02.2021",
            "description": "Метро Санкт-Петербург",
        },
        {
            "amount": -599.8,
            "category": "Ж/д билеты",
            "date": "08.02.2021",
            "description": "РЖД",
        },
    ]


@patch("requests.request")
# создаем мок для получения результата запроса
def test_get_currency_rates(mock_request, currency_list, currency_rates):
    """Тест на получение ответа по запросу о текущем курсе валют."""
    mock_request.return_value.json.return_value = currency_rates
    assert get_currency_rates(currency_list) == [{"currency": "USD", "rate": 97.19}]


@patch("requests.get")
# создаем мок для получения результата запроса
def test_get_stock_prices(mock_get, stock_list, stock_prices):
    """Тест на получение ответа по запросу о стоимости акций из S&P500."""
    mock_get.return_value.json.return_value = stock_prices
    assert get_stock_prices(stock_list) == [{"price": 214.67, "stock": "GOOGL"}]
