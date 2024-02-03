import pandas

from backend.tables.table import Table


class PivotTable(Table):
    def __init__(self, transactions: pandas.DataFrame) -> None:
        super().__init__(transactions)
        self.transaction_table = self.table
        self.transaction_table["month_year"] = self.table["Date"].dt.strftime(
            "%m/%Y"
        )
        self.table = self.transaction_table.pivot_table(
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
