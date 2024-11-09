from src.reports import spending_by_category
from src.services import filter_transactions_by_category, convert_df_to_dict
from src.utils import read_transactions_from_excel_file
from src.views import main_page_with_json_answer

if __name__ == "__main__":
    print(
        main_page_with_json_answer(
            read_transactions_from_excel_file(), "20.02.2021 00:00:00"
        )
    )

    print(filter_transactions_by_category(convert_df_to_dict(read_transactions_from_excel_file())))

    print(
        spending_by_category(
            read_transactions_from_excel_file(),
            "Супермаркеты",
            date="2021.03.31 00:00:00",
        )
    )
