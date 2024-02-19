from injection import pivot_table, investigator_table
from textual.app import ComposeResult
from textual.coordinate import Coordinate
from textual.screen import ModalScreen
from textual.widgets import DataTable, Static

from budget_app.backend.tables.table import Table
from budget_app.widgets.table_widget import TableWidget


class Investigator(ModalScreen):
    BINDINGS = [
        ("x", "close", "Close"),
    ]

    def __init__(self, table: Table) -> None:
        self.table = table
        super().__init__()

    def compose(self) -> ComposeResult:
        yield TableWidget(self.table, "investigator")

    def action_close(self):
        self.dismiss(True)


class Pivot(Static):
    BINDINGS = [("i", "investigate", "Investigate")]

    def compose(self) -> ComposeResult:
        yield TableWidget(pivot_table, "pivot")

    def action_investigate(self) -> None:
        table = self.query_one(DataTable)
        date = str(table.ordered_columns[table.cursor_column].label)
        row_num = table.cursor_row
        category = table.get_cell_at(Coordinate(row_num, 0))
        if date != "Category":
            investigator_table.update_table(date, category)
            self.app.push_screen(
                Investigator(
                    investigator_table,
                )
            )
