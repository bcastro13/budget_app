from budget_app.transactions import transactions
from backend.tables.table import Table


class PivotTable(Table):
    def __init__(self) -> None:
        super().__init__()
        self.table = transactions.table.pivot_table(
            index="Category",
            columns=["month_year"],
            values="Amount",
            aggfunc="sum",
            fill_value=0,
            margins=True,
            margins_name="Total",
        )
        self.table["Selected"] = True
        self.table = self.table.reset_index().reset_index()
        self.ui_table = self.table
