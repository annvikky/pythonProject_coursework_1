import json

from src.services import filter_transactions_by_category


def test_filter_transactions_by_category(transaction_for_filter):
    """Тест на корректность фильтрации операций по переводам физ.лицам."""
    result = filter_transactions_by_category(transaction_for_filter)
    expected = json.dumps(
        [{"Описание": "Иванов И."}, {"Описание": "Петров П."}],
        ensure_ascii=False,
    )
    assert result == expected


def test_filter_transactions_by_category_with_absent_pattern(
    transaction_for_filter_without_requested_value,
):
    """Тест на корректность фильтрации операций по переводам физ.лицам при отсутствии соответствий."""
    result = filter_transactions_by_category(
        transaction_for_filter_without_requested_value
    )
    assert result == []
