import pandas

from backend.tables.table import Table


class PivotTable(Table):
    def __init__(self, transactions: pandas.DataFrame) -> None:
        super().__init__(transactions)
        self.table = self.transactions.table.pivot_table(
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

    def update(self) -> None:
        selected = self.table["Selected"]
        sort_key, ascending = self._get_sort_key()
        self.table = self.transactions.table.pivot_table(
            index="Category",
            columns=["month_year"],
            values="Amount",
            aggfunc="sum",
            fill_value=0,
            margins=True,
            margins_name="Total",
        )
        self.table["Selected"] = selected
        self.table = self.table.reset_index().reset_index()
        self.ui_table = self.table
        self.sort(sort_key, ascending)
