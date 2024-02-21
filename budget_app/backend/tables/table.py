from __future__ import annotations

from abc import ABC

import pandas

from budget_app.transactions import transactions


class Table(ABC):
    def __init__(self) -> None:
        self.ui_table = transactions.table
        self.hidden_columns = ["Selected", "index"]

    def get_columns(self, normal_update: bool) -> list[str]:
        return self._create_ui_table(normal_update).columns.tolist()

    def get_rows(self, normal_update: bool) -> list:
        return self._create_ui_table(normal_update).values.tolist()

    def get_column_values(self, column_name: str) -> list:
        table = (
            transactions.table[[str(column_name), "Selected"]]
            .drop_duplicates()
            .sort_values(
                by=[str(column_name), "Selected"], ascending=[True, False]
            )
            .drop_duplicates(str(column_name))
        )
        table.insert(1, "temp", table[str(column_name)])
        return list(table.itertuples(index=False, name=None))

    def sort(self, sort_key: str, ascending: bool) -> None:
        self.ui_table = self.ui_table.sort_values(
            by=str(sort_key), ascending=ascending
        )
        self.ui_table = self.ui_table.reset_index(drop=True)

    def update_selected(self, column_name: str, selected_values: list) -> None:
        mask = transactions.table[str(column_name)].isin(selected_values)
        transactions.table.loc[~mask, "Selected"] = False
        transactions.table.loc[mask, "Selected"] = True
        self.ui_table = transactions.table[mask]
        self.ui_table = self.ui_table.reset_index(drop=True)

    def edit_cell(
        self,
        column_name: str,
        row_number: int,
        input_value: str,
    ) -> None:
        if column_name == "Date":
            input_value = pandas.to_datetime(input_value)
        elif column_name == "Amount":
            input_value = float(input_value)
        self.ui_table.at[row_number, column_name] = input_value
        transactions.table.at[
            self.ui_table.loc[row_number]["index"], column_name
        ] = input_value
        print(self)
        print(transactions.table)

    def _create_ui_table(self, normal_update: bool) -> pandas.DataFrame:
        print(transactions.table)
        if normal_update:
            self.ui_table = self.ui_table.reset_index(drop=True)
        else:
            self.ui_table = transactions.table
        return self.ui_table.drop(columns=self.hidden_columns)

    def _get_sort_key(self) -> bool | None:
        for column in self.ui_table.columns:
            if self.ui_table[column].is_monotonic_increasing:
                return column, True
            elif self.ui_table[column].is_monotonic_decreasing:
                return column, False
