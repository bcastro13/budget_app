import pandas


class Transactions:
    def __init__(self) -> None:
        self._table = pandas.read_csv(
            "/Users/brandon/Downloads/2023_transactions.csv",
            dtype={
                "Description": "object",
                "Amount": "float64",
                "Category": "object",
                "Account": "object",
            },
        )
        self._table["Date"] = pandas.to_datetime(self._table["Date"])
        self._table = self._table.sort_values(by="Date")
        self._table = self._table.reset_index(drop=True).reset_index()
        self._table["Selected"] = True
        self._table["month_year"] = self._table["Date"].dt.strftime("%m/%Y")

    @property
    def table(self) -> pandas.DataFrame:
        return self._table

    @table.setter
    def table(self, new_table: pandas.DataFrame) -> None:
        self._table = new_table


transactions = Transactions()
