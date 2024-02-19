# import pandas
# import plotext
#
# start_cash = 22576.83
#
# y = plotext.sin() # sinusoidal test signal
# plotext.scatter(y)
# plotext.plotsize(100, 30)
# plotext.title("Scatter Plot") # to apply a title
# plotext.show() # to finally plot
# print(df)
#
# pivot_table = df.pivot_table(
#     index="Category",
#     columns=["month_year"],
#     values="Amount",
#     aggfunc="sum",
#     fill_value=0,
# )
# print(pivot_table)
#
#

from random import randint

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import (
    Digits,
    Footer,
    Label,
    Static,
    TabPane,
    TabbedContent,
)

from budget_app.pages.transactions import Transactions
from budget_app.pages.pivot import Pivot
from budget_app.injection import transaction_table


class Home(Static):
    def compose(self) -> ComposeResult:
        yield Digits(str(randint(1, 10)), id="pi")


class Upload(Static):
    def compose(self) -> ComposeResult:
        yield Label("Upload!")


class Graph(Static):
    def compose(self) -> ComposeResult:
        yield Label("Graph!")


class Budget(Static):
    def compose(self) -> ComposeResult:
        yield Label("Budget!")


class BudgetApp(App):
    TABS = [
        "home",
        "upload",
        "pivot",
        "graph",
        "budget",
        "transactions",
        "testig",
    ]

    def compose(self) -> ComposeResult:
        yield Footer()

        with TabbedContent(id="tabs"):
            with TabPane("Home", id="home"):
                yield Home()
            with TabPane("Upload", id="upload"):
                yield Upload()
            with TabPane("Pivot", id="pivot"):
                yield Pivot()
            with TabPane("Graph", id="graph"):
                yield Graph()
            with TabPane("Budget", id="budget"):
                yield Budget()
            with TabPane("Transactions", id="transactions"):
                yield Transactions()

    @on(TabbedContent.TabActivated)
    def refresh_table(self) -> None:
        table = self.query("#transactions_table").first()
        table.clear(columns=True)
        table.add_columns(*transaction_table.get_columns())
        table.add_rows(transaction_table.get_rows())


if __name__ == "__main__":
    BudgetApp().run()
