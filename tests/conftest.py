import pandas as pd
import pytest


@pytest.fixture
def transaction_by_date():
    return pd.DataFrame(
        [
            {
                "Дата операции": "10.04.2021 19:37:03",
                "Сумма операции": -85000.0,
                "Категория": "Переводы",
                "Описание": "Николай Н.",
            },
            {
                "Дата операции": "16.06.2021 19:37:03",
                "Сумма операции": -4800.0,
                "Категория": "Связь",
                "Описание": "Sknt.Ru",
            },
            {
                "Дата операции": "13.07.2021 19:37:03",
                "Сумма операции": -812.3,
                "Категория": "Аптеки",
                "Описание": "Аптека Вита",
            },
            {
                "Дата операции": "04.02.2021 19:37:03",
                "Сумма операции": -700.0,
                "Категория": "Транспорт",
                "Описание": "Метро Санкт-Петербург",
            },
            {
                "Дата операции": "08.02.2021 18:32:26",
                "Сумма операции": -599.8,
                "Категория": "Ж/д билеты",
                "Описание": "РЖД",
            },
        ]
    )


@pytest.fixture
def transaction_by_date_filtered():
    return pd.DataFrame(
        [
            {
                "Дата операции": "04.02.2021 19:37:03",
                "date": "2021-02-04 19:37:03",
                "Сумма операции": -700.0,
                "Категория": "Транспорт",
                "Описание": "Метро Санкт-Петербург",
            },
            {
                "Дата операции": "08.02.2021 18:32:26",
                "date": "2021-02-08 18:32:26",
                "Сумма операции": -599.8,
                "Категория": "Ж/д билеты",
                "Описание": "РЖД",
            },
        ]
    )


@pytest.fixture
def transaction_by_card_1():
    return pd.DataFrame(
        [
            {"Номер карты": "1112", "Сумма платежа": -46207.08, "Кэшбек": 462.07},
            {"Номер карты": "4556", "Сумма платежа": 533948.75, "Кэшбек": 5339.49},
        ]
    )


@pytest.fixture
def transaction_by_card_2():
    return pd.DataFrame(
        [
            {"Номер карты": "1112", "Сумма платежа": -46207.08, "Кэшбек": 462.07},
            {"Номер карты": "1112", "Сумма платежа": 533948.75, "Кэшбек": 5339.49},
        ]
    )


@pytest.fixture
def top_transaction():
    return pd.DataFrame(
        [
            {
                "Дата платежа": "10.02.2021",
                "Сумма операции": -85000.0,
                "Категория": "Переводы",
                "Описание": "Николай Н.",
            },
            {
                "Дата платежа": "16.02.2021",
                "Сумма операции": -4800.0,
                "Категория": "Связь",
                "Описание": "Sknt.Ru",
            },
            {
                "Дата платежа": "13.02.2021",
                "Сумма операции": -812.3,
                "Категория": "Аптеки",
                "Описание": "Аптека Вита",
            },
            {
                "Дата платежа": "04.02.2021",
                "Сумма операции": -700.0,
                "Категория": "Транспорт",
                "Описание": "Метро Санкт-Петербург",
            },
            {
                "Дата платежа": "08.02.2021",
                "Сумма операции": -599.8,
                "Категория": "Ж/д билеты",
                "Описание": "РЖД",
            },
        ]
    )


@pytest.fixture
def currency_list():
    return ["USD"]


@pytest.fixture
def currency_rates():
    return {
        "success": True,
        "timestamp": 1729967705,
        "base": "USD",
        "date": "2024-10-26",
        "rates": {"RUB": 97.190373},
    }


@pytest.fixture
def stock_list():
    return ["GOOGL"]


@pytest.fixture
def stock_prices():
    return {
        "Global Quote": {
            "01. symbol": "GOOGL",
            "02. open": "216.8000",
            "03. high": "218.6500",
            "04. low": "214.3850",
            "05. price": "214.6700",
            "06. volume": "8482235",
            "07. latest trading day": "2024-10-25",
            "08. previous close": "218.3900",
            "09. change": "-3.7200",
            "10. change percent": "-1.7034%",
        }
    }


@pytest.fixture
def transaction_for_report():
    return pd.DataFrame(
        [
            {
                "Дата операции": "31.03.2023 00:00:00",
                "Сумма операции": -544.34,
                "Категория": "Супермаркеты",
            },
            {
                "Дата операции": "31.03.2021 00:00:00",
                "Сумма операции": -342.50,
                "Категория": "Связь",
            },
            {
                "Дата операции": "17.03.2021 00:00:00",
                "Сумма операции": -10000.00,
                "Категория": "Одежда",
            },
            {
                "Дата операции": "15.02.2021 00:00:00",
                "Сумма операции": -944.34,
                "Категория": "Супермаркеты",
            },
            {
                "Дата операции": "01.01.2021 00:00:00",
                "Сумма операции": -644.34,
                "Категория": "Супермаркеты",
            },
        ]
    )


@pytest.fixture
def transaction_for_filter():
    return pd.DataFrame(
        [
            {"Описание": "Иванов И."},
            {"Описание": "Петров П."},
            {"Описание": "Перевод с карты"},
        ]
    )


@pytest.fixture
def transaction_for_filter_without_requested_value():
    return pd.DataFrame(
        [{"Описание": "Колхоз"}, {"Описание": "МТС"}, {"Описание": "Перевод с карты"}]
    )


# Добрый вечер!
# [{'last_digits': '1112', 'total_spent': -46207.08, 'cashback': 462.07}, {'last_digits': '4556', 'total_spent': 533948.75, 'cashback': 5339.49}, {'last_digits': '5091', 'total_spent': -14918.16, 'cashback': 149.18}, {'last_digits': '5441', 'total_spent': -470854.8, 'cashback': 4708.55}, {'last_digits': '5507', 'total_spent': -84000.0, 'cashback': 840.0}, {'last_digits': '6002', 'total_spent': -69200.0, 'cashback': 692.0}, {'last_digits': '7197', 'total_spent': -2417014.58, 'cashback': 24170.15}]
# [{'date': '21.03.2019', 'amount': -190044.51, 'category': 'Переводы', 'description': 'Перевод Кредитная карта. ТП 10.2 RUR'}, {'date': '21.03.2019', 'amount': 190044.51, 'category': 'Переводы', 'description': 'Перевод Кредитная карта. ТП 10.2 RUR'}, {'date': '27.07.2018', 'amount': -179571.56, 'category': nan, 'description': 'Перевод средств с брокерского счета'}, {'date': '27.07.2018', 'amount': -179571.56, 'category': nan, 'description': 'Перевод средств с брокерского счета'}, {'date': '28.07.2018', 'amount': -179571.56, 'category': nan, 'description': 'Перевод средств с брокерского счета'}]
# {'USD': 0.010289, 'EUR': 0.009527}
# [{'stock': 'AAPL', 'price': 231.41}, {'stock': 'AMZN', 'price': 187.83}, {'stock': 'GOOGL', 'price': 165.27}, {'stock': 'MSFT', 'price': 428.15}, {'stock': 'TSLA', 'price': 269.19}]
