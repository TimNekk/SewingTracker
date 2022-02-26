from typing import Union, List, Optional

import gspread
from gspread.utils import ValueRenderOption
from oauth2client.service_account import ServiceAccountCredentials


class Sheets:
    def __init__(self, credentials: ServiceAccountCredentials, input_sheet_name: str = "input", models_start_row: int = 4, models_start_column: int = 1,
                 markets_names_row: int = 3, models_names_column: int = 1):
        self.client = gspread.authorize(credentials)
        self.workbook = self.client.open("SewingTracker")
        self.input_sheet_name = input_sheet_name
        self.sheet = self.get_input_sheet()

        self.models_start_row = models_start_row
        self.models_start_column = models_start_column

        self.markets_names_row = markets_names_row
        self.models_names_column = models_names_column

    def get_input_sheet(self) -> gspread.Worksheet:
        return self.workbook.worksheet(self.input_sheet_name)

    def get_models(self) -> str:
        return self.sheet.col_values(self.models_start_column)[self.models_start_row-1:]

    def edit_model_market_cell(self, model_name: str, market_name: str, value: Union[int, str, float]) -> None:
        self.sheet.update_cell(self.sheet.find(model_name).row, self.sheet.find(market_name).col, value)

    def add_model(self, model_name: str) -> None:
        self.sheet.update_cell(len(self.sheet.col_values(self.models_start_column)) + 1, self.models_start_column, model_name)

    def get_cells(self, clear=False) -> List[List[str]]:
        cells = self.sheet.get_all_values(value_render_option=ValueRenderOption.unformatted)

        if clear:
            for row in range(len(cells)):
                if row < 3:
                    continue
                for col in range(len(cells[row])):
                    if col == 3 or col > 4:
                        cells[row][col] = ''

        return cells

    def get_markets_column(self, cells: Optional[List[List[str]]] = None) -> List[str]:
        if not cells:
            cells = self.get_cells()
        return cells[self.markets_names_row - 1]

    def get_models_column(self, cells: Optional[List[List[str]]] = None) -> List[str]:
        if not cells:
            cells = self.get_cells()
        return list(map(lambda row: row[self.models_names_column - 1], cells))

    def update_cells(self, cells: List[List[str]], start: str = "A1") -> None:
        for row_index in range(len(cells)):
            for cell_index in range(len(cells[0])):
                if cells[row_index][cell_index] == "+":
                    cells[row_index][cell_index] = "'+"
        self.sheet.update(start, cells, value_input_option="USER_ENTERED")
