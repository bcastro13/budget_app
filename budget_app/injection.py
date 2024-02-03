import pandas

from backend.tables.transaction_table import TransactionsTable
from backend.tables.pivot_table import PivotTable
from budget_app.backend.tables.investigator_table import InvestigatorTable

transactions = pandas.read_csv(
    "/Users/brandon/Downloads/2023_transactions.csv",
    dtype={
        "Description": "object",
        "Amount": "float64",
        "Category": "object",
        "Account": "object",
    },
)
transactions["Date"] = pandas.to_datetime(transactions["Date"])
transactions = transactions.sort_values(by="Date")
transactions = transactions.reset_index(drop=True).reset_index()
transactions["Selected"] = True

transaction_table = TransactionsTable(transactions)
pivot_table = PivotTable(transactions)
investigator_table = InvestigatorTable(transactions)
