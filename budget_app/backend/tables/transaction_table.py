import pandas

from backend.tables.table import Table


class TransactionsTable(Table):
    def __init__(self, transactions: pandas.DataFrame) -> None:
        super().__init__(transactions)
