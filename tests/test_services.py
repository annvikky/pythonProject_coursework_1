import json

import pytest

from src.services import filter_transactions_by_category, convert_df_to_dict


def test_convert_df_to_dict(transaction_for_report):
    result = convert_df_to_dict(transaction_for_report)
    assert result == [
        {
            "Дата операции": "31.03.2023 00:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": -544.34,
        },
        {
            "Дата операции": "31.03.2021 00:00:00",
            "Категория": "Связь",
            "Сумма операции": -342.5,
        },
        {
            "Дата операции": "17.03.2021 00:00:00",
            "Категория": "Одежда",
            "Сумма операции": -10000.0,
        },
        {
            "Дата операции": "15.02.2021 00:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": -944.34,
        },
        {
            "Дата операции": "01.01.2021 00:00:00",
            "Категория": "Супермаркеты",
            "Сумма операции": -644.34,
        },
    ]


def test_convert_df_to_dict_with_wrong_attribute():
    """Тест на обработку некорректного атрибута."""
    assert convert_df_to_dict("") == []


def test_filter_transactions_by_category_with_pattern(transaction_for_filter):
    """Тест на корректность фильтрации операций по переводам физ.лицам."""
    result = filter_transactions_by_category(transaction_for_filter)
    expected = (
        '[{"Категория": "Переводы", "Описание": "Иванов И."},'
        ' {"Категория": "Переводы", "Описание": "Петров П."}]'
    )
    assert result == expected


def test_filter_transactions_by_category_with_absent_pattern(
    transaction_for_filter_without_requested_value,
):
    """Тест на корректность фильтрации при отсутствии соответствий."""
    result = filter_transactions_by_category(
        transaction_for_filter_without_requested_value
    )
    assert result == []


@pytest.mark.parametrize(
    "dict_list, expected",
    [
        (
            [
                {"Категория": "Переводы", "Описание": "Иванов И."},
                {"Категория": "Оплата услуги", "Описание": "АЗС"},
                {"Категория": "Переводы", "Описание": "Пополнение карты"},
            ],
            json.dumps(
                [
                    {"Категория": "Переводы", "Описание": "Иванов И."},
                ],
                ensure_ascii=False,
            ),
        ),
        (
            [
                {"Категория": "Платеж", "Описание": "Оплата обучения"},
                {"Категория": "Платеж", "Описание": "Супермаркет"},
            ],
            [],
        ),
    ],
)
def test_filter_transactions_by_category(dict_list, expected):
    result = filter_transactions_by_category(dict_list)
    assert result == expected
