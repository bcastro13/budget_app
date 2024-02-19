from injection import transaction_table
from textual.app import ComposeResult
from textual.widgets import Static

from budget_app.widgets.table_widget import TableWidget


class Transactions(Static):
    def compose(self) -> ComposeResult:
        yield TableWidget(transaction_table, "transactions_table")
