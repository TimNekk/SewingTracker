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

        # row = self.models_start_row
        # while True:
        #     model = self.sheet.cell(row, self.models_start_column).value
        #     if not model:
        #         break
        #
        #     price = self.sheet.cell(row, self.models_start_column + 1).value
        #     models[model] = price
        #     row += 1
        #
        # return models

        # models_rows = map(lambda row: (row[0], 0 if row[1] is None else row[1]),
        #                   filter(lambda row: row[0] is not None,
        #                          self.input_sheet.iter_rows(min_row=self.models_start_cell[0],
        #                                          min_col=self.models_start_cell[1],
        #                                          max_row=self.models_end_cell[0],
        #                                          max_col=self.models_end_cell[1],
        #                                          values_only=True)
        #                          )
        #                   )
        #
        # return dict(models_rows)

    # def create_temp_model_file(self, model: Model, market: Optional[str] = None) -> None:
    #     temp_workbook = openpyxl.Workbook()
    #     sheet: Worksheet = temp_workbook.worksheets[0]
    #     sheet.title = model.name
    #     sheet.cell(1, 1).value = "Дата"
    #     sheet.cell(1, 1).hyperlink = "test"
    #     sheet.sheet_format.baseColWidth = 17
    #
    #     if market:
    #         sheet.cell(1, 2, "Цена")
    #         sheet.title = f"{model.name} ({market})"
    #         self._load_market_prices(sheet, model.get_history(), market)
    #     else:
    #         self._load_markets_prices(sheet, model.get_history())
    #
    #     filename = f"{self.temp_directory}\\{uuid4()}.xlsx"
    #     temp_workbook.save(filename)
    #     os.system(filename)

    # @staticmethod
    # def _load_market_prices(sheet: Worksheet, history: ModelHistory, market: str) -> None:
    #     points = tuple(filter(lambda point: point.prices.get(market), history.points))
    #     sheet["A1"].font = Font(bold=True)
    #
    #     # First point
    #     sheet.cell(2, 1, points[0].date)
    #     sheet.cell(2, 2, points[0].prices.get(market))
    #     sheet[f"A2"].font = Font(bold=True)
    #
    #     row_index = 3
    #     for points_index in range(1, len(points)):
    #         previous_point, current_point = points[points_index - 1], points[points_index]
    #         previous_price, current_price = previous_point.prices.get(market), current_point.prices.get(market)
    #
    #         if not current_price or not previous_price:
    #             continue
    #
    #         if current_price != previous_price:
    #             sheet.cell(row_index, 2, current_price)
    #             sheet.cell(row_index, 1, current_point.date)
    #             sheet[f"A{row_index}"].font = Font(bold=True)
    #             row_index += 1
    #
    # @staticmethod
    # def _load_markets_prices(sheet: Worksheet, history: ModelHistory) -> None:
    #     # Markets
    #     for markets_index, market in enumerate(db.markets):
    #         sheet.cell(1, markets_index + 2, market)
    #
    #     points = history.points
    #     sheet["A1"].font = Font(bold=True)
    #
    #     # First point
    #     sheet.cell(2, 1, points[0].date)
    #     sheet[f"A2"].font = Font(bold=True)
    #     for price_index, price in enumerate(points[0].prices.values()):
    #         sheet.cell(2, price_index + 2, price)
    #
    #     row_index = 3
    #     for points_index in range(1, len(points)):
    #         previous_point, current_point = points[points_index - 1], points[points_index]
    #         added = False
    #
    #         for markets_index, (market, current_price) in enumerate(current_point.prices.items()):
    #             previous_price = previous_point.prices.get(market)
    #
    #             if not current_price or not previous_price:
    #                 continue
    #
    #             if current_price != previous_price:
    #                 sheet.cell(row_index, markets_index + 2, current_price)
    #                 added = True
    #
    #         if added:
    #             sheet.cell(row_index, 1, current_point.date)
    #             sheet[f"A{row_index}"].font = Font(bold=True)
    #             row_index += 1

    def edit_model_market_cell(self, model_name: str, market_name: str, value: Union[int, str, float]) -> None:
        self.sheet.update_cell(self.sheet.find(model_name).row, self.sheet.find(market_name).col, value)

    def add_model(self, model_name: str) -> None:
        self.sheet.update_cell(len(self.sheet.col_values(self.models_start_column)) + 1, self.models_start_column, model_name)

    def clear_sheet(self) -> None:
        self.sheet.batch_clear(["D4:D1000", "F4:FF1000"])

    def get_cells(self) -> List[List[str]]:
        return self.sheet.get_all_values(value_render_option=ValueRenderOption.unformatted)

    def get_markets_column(self, cells: Optional[List[List[str]]] = None) -> List[str]:
        if not cells:
            cells = self.get_cells()
        return cells[self.markets_names_row - 1]

    def get_models_column(self, cells: Optional[List[List[str]]] = None) -> List[str]:
        if not cells:
            cells = self.get_cells()
        return list(map(lambda row: row[self.models_names_column - 1], cells))

    def update_cells(self, cells: List[List[str]], start: str = "A1") -> None:
        self.sheet.update(start, cells)


if __name__ == "__main__":
    from data.config import credentials

    sheets = Sheets(credentials)