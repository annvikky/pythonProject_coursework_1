import json
import logging
import os
import re

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


def filter_transactions_by_category(df: pd.DataFrame) -> json:
    """Функция для поиска транзакции по категории Переводы физ. лицам."""
    filtered_transactions = []
    df = df.to_dict(orient="records")
    pattern = r"\b[А-Я][а-я]+\s[А-Я]\."
    for transaction in df:
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


# print(filter_transactions_by_category(read_transactions_from_excel_file()))
