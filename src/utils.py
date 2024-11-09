import logging
import os.path
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

path_to_exl = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "operations.xlsx"
)

load_dotenv()
apikey = os.getenv("API_KEY")
apikey_2 = os.getenv("apikey_2")


logger = logging.getLogger("reader")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs/reader.log"),
    mode="w",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transactions_from_excel_file() -> pd.DataFrame | None:
    try:
        return pd.read_excel(path_to_exl)
    except Exception as e:
        logger.info(f"Недоступно для чтения. Ошибка: {e}")
        raise e


def get_greeting():
    """Функция приветствия относительно текущего времени суток."""
    now = datetime.now()
    current_hour = now.hour
    if 3 < int(current_hour) < 12:
        greeting = "Доброе утро!"
        logger.info("Утреннее приветствие выполнено")
        return greeting
    elif 12 <= int(current_hour) <= 16:
        greeting = "Добрый день!"
        logger.info("Дневное приветствие выполнено")
        return greeting
    elif 17 <= int(current_hour) <= 23:
        greeting = "Добрый вечер!"
        logger.info("Вечернее приветствие выполнено")
        return greeting
    else:
        greeting = "Доброй ночи!"
        logger.info("Ночное приветствие выполнено")
        return greeting


def filter_info_by_date(current_date, df):
    """Функция фильтрации информации с начала месяца на текущую дату."""
    try:
        logger.info("Период для фильтрации получен.")
        end = datetime.strptime(current_date, "%d.%m.%Y %H:%M:%S")
        start = datetime.strptime(
            f"01.{end.month}.{end.year} 00:00:00", "%d.%m.%Y %H:%M:%S"
        )
        logger.info("Преобразование даты.")
        df["date"] = df["Дата операции"].map(
            lambda x: datetime.strptime(x, "%d.%m.%Y %H:%M:%S")
        )
        logger.info("Операции по периоду отфильтрованы")
        filtered_transactions = df[(df["date"] >= start) & (df["date"] <= end)]
        return filtered_transactions
    except ValueError as e:
        logger.error(e)
        print("Неверный формат даты. Введите дату в формате DD.MM.YY HH:MM:SS")


print(filter_info_by_date("20.02.2021 00:00:00", read_transactions_from_excel_file()))


def filter_info_by_card(filtered_transactions: pd.DataFrame):
    """Функция для сортировки информации по операциям в разрезе карт."""

    filtered_transactions = filtered_transactions.rename(
        columns={
            "Номер карты": "last_digits",
            "Сумма платежа": "total_spent",
            "Кэшбек": "cashback",
        }
    )
    filtered_info = filtered_transactions.groupby(["last_digits"], as_index=False).agg(
        {"total_spent": "sum"}
    )
    filtered_info["cashback"] = filtered_info["total_spent"].apply(
        lambda x: round(abs(x) / 100, 2)
    )
    filtered_info["last_digits"] = filtered_info["last_digits"].apply(
        lambda x: x.replace("*", "")
    )
    data_list = filtered_info.to_dict("records")
    logger.info("Данные по картам успешно сформированы")
    return data_list


def get_top_transactions(transactions: pd.DataFrame):
    """Функция для вывода информации о последних пяти транзакциях."""

    last_transactions = transactions.sort_values(
        by="Сумма операции", ascending=False, key=lambda x: abs(x)
    )
    last_transactions = last_transactions[0:5]
    top_transactions = []
    for index, row in last_transactions.iterrows():
        top_transaction = {
            "date": row["Дата платежа"],
            "amount": round(row["Сумма операции"], 2),
            "category": row["Категория"],
            "description": row["Описание"],
        }
        top_transactions.append(top_transaction)
    logger.info("Топ-5 транзакций сформированы.")

    return top_transactions


def get_currency_rates(currency_list):
    """Функция для получения текущего курса валют"""
    try:
        rates = []
        for currency in currency_list:
            url = f"https://api.apilayer.com/fixer/latest?symbols=RUB&base={currency}"

            headers = {"apikey": apikey}
            response = requests.request("GET", url, headers=headers)
            result = response.json()
            rates.append(
                {"currency": currency, "rate": round(result["rates"]["RUB"], 2)}
            )
        logger.info("Курсы валют на текущую дату получены.")
        return rates
    except KeyError:
        logger.error(
            "Получение курса валют: ошибка ввода apikey или превышен дневной лимит запросов."
        )
        return 0


def get_stock_prices(stock_list) -> object:
    """Функция для получения стоимости акций из S&P500."""
    try:
        stock_prices = []
        for stock in stock_list:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={apikey_2}"
            r = requests.get(url)
            data = r.json()
            stock = data["Global Quote"]["01. symbol"]
            price = data["Global Quote"]["05. price"]
            new_dict = {"stock": stock, "price": round(float(price), 2)}
            stock_prices.append(new_dict)
        logger.info("Данные по акциям успешно выведены.")
        return stock_prices
    except KeyError:
        logger.error(
            "Получение данных по акциям: ошибка ввода apikey или превышен дневной лимит запросов."
        )
        return 0
