import json
import logging
import os
import re
from typing import List, Dict

import pandas as pd

from src.utils import read_transactions_from_excel_file

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs/services.log"),
    mode="w",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def convert_df_to_dict(df: pd.DataFrame):
    """Получаем список словарей."""
    dict_list = []
    try:
        for _, row in df.iterrows():
            dictionary = {}
            for column in df.columns:
                dictionary[column] = row[column]
            dict_list.append(dictionary)

        logger.info("Список словарей для дальнейшей фильтрации получен.")
        return dict_list
    except:
        logger.warning("Переданный аргумент не содержит DataFrame.")
        return []


# print(convert_pd_to_dict(read_transactions_from_excel_file()))


def filter_transactions_by_category(dict_list: List[Dict]) -> json:
    """Функция для поиска транзакции по категории Переводы физ. лицам. Принимает транзакции в формате списка
    словарей."""
    filtered_transactions = []
    pattern = r"\b[А-Я][а-я]+\s[А-Я]\."
    for transaction in dict_list:
        if transaction.get("Категория") == "Переводы":
            if "Описание" in transaction and re.match(pattern, transaction["Описание"]):
                filtered_transactions.append(transaction)
    logger.info(
        f"Найдено {len(filtered_transactions)} транзакций, соответствующих заданным критериям"
    )

    if filtered_transactions:
        filtered_transactions_to_json = json.dumps(
            filtered_transactions, ensure_ascii=False
        )
        logger.info(f"Возвращен json-ответ с {len(filtered_transactions)} транзакций")
        return filtered_transactions_to_json
    else:
        logger.info("Совпадений не найдено")
        return []


# print(filter_transactions_by_category(convert_pd_to_dict(read_transactions_from_excel_file())))
if __name__ == "__main__":
    print(
        filter_transactions_by_category(
            convert_df_to_dict(read_transactions_from_excel_file())
        )
    )
