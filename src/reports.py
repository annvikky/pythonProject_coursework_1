import json
import logging
import os
import datetime
from functools import wraps

import pandas as pd

from src.utils import read_transactions_from_excel_file

path_to_json_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "report_spending_by_category.json",
)
path_to_json_file_as_arg = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "report.json"
)

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs/reports.log"),
    mode="w",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def decorator_without_args(function):
    """Декоратор, указывающий файл записи данных из отчета."""

    def wrapper(*args, **kwargs):
        try:
            logger.info("Запись данных в файл 'report_spending_by_category'")
            result = function(*args, **kwargs)
            result.to_json(
                path_to_json_file="report",
                orient="records",
                indent=4,
                force_ascii=False,
            )
            return result
        except Exception as e:
            print(f"Неудачная попытка записи данных в файл. Ошибка: {e}")
            logger.error(f"Неудачная попытка записи данных в файл. Ошибка: {e}")
        return wrapper


def decorator_with_args(file_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                logger.info("Записываем данные в файл 'report'")
                result = func(*args, **kwargs)
                result.to_json(file_name, orient="records", indent=4, force_ascii=False)
                return result
            except Exception as e:
                print(f"Неудачная попытка записи данных в файл. Ошибка: {e}")
                logger.error(f"Неудачная попытка записи данных в файл. Ошибка: {e}")

        return wrapper

    return decorator


@decorator_with_args(path_to_json_file_as_arg)
def spending_by_category(
    transactions: pd.DataFrame, category, date=None
) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    transactions["Дата операции"] = transactions["Дата операции"].apply(
        lambda x: datetime.datetime.strptime(x, "%d.%m.%Y %H:%M:%S").date()
    )

    try:
        if date:
            end_date = datetime.datetime.strptime(date, "%Y.%m.%d %H:%M:%S").date()
            start_date = end_date - datetime.timedelta(days=90)
            logger.info(f"Передана дата окончания периода отчета: {date}")
        else:
            end_date = datetime.datetime.now().date()
            start_date = end_date - datetime.timedelta(days=90)
            logger.info("f'Дата окончания периода отчета: {date}'")
        report_by_category = transactions.loc[
            (transactions["Дата операции"] <= end_date)
            & (transactions["Дата операции"] >= start_date)
            & (transactions["Категория"] == category)
        ]
        report_by_category.loc["Дата операции"] = report_by_category[
            "Дата операции"
        ].apply(lambda x: x.strftime("%d.%m.%Y"))
        logger.info("Выборка операций успешно завершена")
        count = len(report_by_category)
        logger.info(f"Найдено {count-1} операций.")
        # report_by_category.dropna(inplace=True)
        return report_by_category

    except ValueError as e:
        logger.error(f"Некорректный формат даты. Ошибка: {e}")
        print("Некорректный формат даты")
        return pd.DataFrame({})


# print(spending_by_category(read_transactions_from_excel_file(), "Супермаркеты", date="2021.03.31 00:00:00"))
