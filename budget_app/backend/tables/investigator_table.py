from backend.tables.table import Table
from budget_app.transactions import transactions


class InvestigatorTable(Table):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_columns.append("month_year")

    def update_table(self, date: str, category: str) -> None:
        self.ui_table = transactions.table[
            transactions.table["month_year"] == date
        ]

        if category != "Total":
            self.ui_table = self.ui_table[
                self.ui_table["Category"] == category
            ]
