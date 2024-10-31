from src.reports import spending_by_category


def test_spending_by_category(transaction_for_report):
    """Тест на корректную фильтрацию операций по заданной категории и переданному времени"""
    result = spending_by_category(
        transaction_for_report, "Супермаркеты", date="2021.03.31 00:00:00"
    )
    result.dropna(inplace=True)
    assert len(result) == 2


def test_spending_by_absent_category(transaction_for_report):
    """Тест на корректную фильтрацию операций при отсутствии заданной категории и переданному времени"""
    result = spending_by_category(
        transaction_for_report, "Магазины", date="2021.03.31 00:00:00"
    )
    result.dropna(inplace=True)
    assert len(result) == 0


def test_spending_by_category_without_date(transaction_for_report):
    """Тест на корректную фильтрацию операций по заданной категории и переданному времени"""
    result = spending_by_category(transaction_for_report, "Супермаркеты")
    result.dropna(inplace=True)
    assert len(result) == 0
