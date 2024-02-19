from __future__ import annotations

from itertools import cycle
from typing import TYPE_CHECKING

from textual.screen import ModalScreen
from textual.widgets import (
    DataTable,
    Footer,
    Input,
    SelectionList,
    Static,
)

from budget_app.injection import (
    table_updater,
)


if TYPE_CHECKING:
    from textual.app import ComposeResult
    from backend.tables.table import Table


class FilterSelector(ModalScreen):
    BINDINGS = [
        ("x", "close", "Close"),
    ]

    def __init__(self, table: Table, column_name: str) -> None:
        self.table = table
        self.column_name = column_name
        super().__init__()

    def compose(self) -> ComposeResult:
        column_values = self.table.get_column_values(self.column_name)
        yield SelectionList(*column_values)
        yield Footer()

    def action_close(self):
        selection_list = self.query_one(SelectionList)
        self.table.update_selected(self.column_name, selection_list.selected)
        self.dismiss(True)


class CellEditor(ModalScreen):
    BINDINGS = [
        ("enter", "submit", "submit"),
    ]

    def __init__(
        self,
        table: Table,
        column_name: str,
        row_number: int,
        input_value: str,
    ) -> None:
        self.table = table
        self.column_name = str(column_name)
        self.row_number = row_number
        self.input_value = str(input_value)
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Input(self.input_value)

    def key_enter(self):
        input_field = self.query_one(Input)
        self.table.edit_cell(
            self.column_name, self.row_number, input_field.value
        )
        table_updater.update_tables()
        print(self.table.transactions.table)
        self.dismiss(True)


class TableWidget(Static):
    BINDINGS = [
        ("s", "sort_column()", "Sort Column"),
        ("f", "filter_table", "Filter Table"),
        ("e", "edit_cell", "Edit Cell"),
    ]
    CURSORS = cycle(["column", "row", "cell"])

    current_sorts = set()

    def __init__(self, table, id=None) -> None:
        self.table = table
        self.table_id = id
        super().__init__()

    def compose(self) -> ComposeResult:
        yield DataTable(id=self.table_id)

    def on_mount(self) -> None:
        data_table = self.query_one(DataTable)
        data_table.add_columns(*self.table.get_columns())
        data_table.add_rows(self.table.get_rows())

    def action_sort_column(self) -> None:
        print(self.table.transactions.table)
        table = self.query_one(DataTable)
        sort_key = table.ordered_columns[table.cursor_column].label
        self.table.sort(sort_key, self.sort_reverse(sort_key))
        self.update_table(True)

    def sort_reverse(self, sort_type: str) -> bool:
        sort_type = str(sort_type)
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    def action_filter_table(self) -> None:
        table = self.query_one(DataTable)
        column_name = table.ordered_columns[table.cursor_column].label
        self.app.push_screen(
            FilterSelector(self.table, column_name), self.update_table
        )

    def action_edit_cell(self) -> None:
        table = self.query_one(DataTable)
        column_name = table.ordered_columns[table.cursor_column].label
        row_number = table.cursor_row
        self.app.push_screen(
            CellEditor(
                self.table,
                column_name,
                row_number,
                table.get_cell_at(table.cursor_coordinate),
            ),
            self.update_table,
        )

    def update_table(self, val: bool):
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*self.table.get_columns())
        table.add_rows(self.table.get_rows())
