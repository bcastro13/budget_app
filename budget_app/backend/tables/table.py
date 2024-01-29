from abc import ABC

import pandas


class Table(ABC):
    def __init__(self, transactions: pandas.DataFrame) -> None:
        self.table = transactions
        self.hidden_columns = ["Selected", "index"]
        self.ui_table = self.table

    def get_columns(self) -> list[str]:
        return self._create_ui_table().columns.tolist()

    def get_rows(self) -> list:
        return self._create_ui_table().values.tolist()

    def get_column_values(self, column_name: str) -> list:
        table = (
            self.table[[str(column_name), "Selected"]]
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
        mask = self.table[str(column_name)].isin(selected_values)
        self.table.loc[~mask, "Selected"] = False
        self.table.loc[mask, "Selected"] = True
        self.ui_table = self.table[mask]
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
        self.table.at[
            self.ui_table.loc[row_number]["index"], column_name
        ] = input_value

    def _create_ui_table(self) -> pandas.DataFrame:
        self.ui_table = self.ui_table.reset_index(drop=True)
        return self.ui_table.drop(columns=self.hidden_columns)
