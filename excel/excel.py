import logging
from typing import Union

import openpyxl
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class ExcelHandler:
    def __init__(self, input_file_path: str, input_sheet_name: str = "input", models_start_cell: tuple = (4, 1), models_end_cell: tuple = (100, 20),
                 markets_names_row: int = 3, models_names_column: int = 1):
        self.file = input_file_path
        self.workbook

        self.models_start_cell = models_start_cell
        self.models_end_cell = models_end_cell

        self.markets_names_row = markets_names_row
        self.models_names_column = models_names_column

        self.input_sheet_name = input_sheet_name
        self._check_input_sheet()

    def _check_input_sheet(self) -> None:
        if self.input_sheet_name not in self.workbook.sheetnames:
            raise ValueError(f"Input sheet \"{self.input_sheet_name}\" not found!")

    @property
    def workbook(self) -> Workbook:
        return openpyxl.load_workbook(self.file, keep_vba=True)

    @property
    def input_sheet(self) -> Worksheet:
        return self.workbook[self.input_sheet_name]

    def save(self, workbook: Workbook) -> None:
        try:
            workbook.save(self.file)
        except PermissionError:
            logging.error(f"Close file {self.file}")

    def get_models(self) -> dict[str: int]:
        sheet = self.input_sheet

        models_rows = map(lambda row: (row[0], 0 if row[1] is None else row[1]),
                                       filter(lambda row: row[0] is not None,
                                              sheet.iter_rows(min_row=self.models_start_cell[0],
                                                              min_col=self.models_start_cell[1],
                                                              max_row=self.models_end_cell[0],
                                                              max_col=self.models_end_cell[1],
                                                              values_only=True)
                                              )
                                       )

        return dict(models_rows)

    def edit_model_market_cell(self, model_name: str, market_name: str, value: Union[int, str, float]) -> None:
        market_column_index = self.get_market_column_index(market_name)
        model_row_index = self.get_model_row_index(model_name)

        workbook = self.workbook
        sheet = workbook[self.input_sheet_name]
        sheet.cell(model_row_index, market_column_index, value)
        self.save(workbook)

    def get_market_column_index(self, market_name: str) -> int:
        sheet = self.input_sheet
        markets_ids_row = list(map(lambda cell: cell.value, list(sheet.rows)[self.markets_names_row - 1]))
        return markets_ids_row.index(market_name) + 1

    def get_model_row_index(self, model_name: str) -> int:
        sheet = self.input_sheet
        models_names_column = list(map(lambda cell: cell.value, list(sheet.columns)[self.models_names_column - 1]))
        return models_names_column.index(model_name) + 1

    def create_temp_file(self):
        workbook = openpyxl.Workbook()
