from budget_app.backend.tables.table import Table


class TableUpdater:
    def __init__(self, tables: list[Table]) -> None:
        self.tables = tables

    def update_tables(self) -> None:
        for table in self.tables:
            print(table.transactions.table)
            table.update()
