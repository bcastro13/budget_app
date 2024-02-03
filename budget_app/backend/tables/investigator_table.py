import pandas

from backend.tables.table import Table


class InvestigatorTable(Table):
    def __init__(self, transactions: pandas.DataFrame) -> None:
        super().__init__(transactions)
        self.hidden_columns.append("month_year")

    def update_table(self, date: str, category: str) -> None:
        self.ui_table = self.table[self.table["month_year"] == date]

        if category != "Total":
            self.ui_table = self.ui_table[
                self.ui_table["Category"] == category
            ]
