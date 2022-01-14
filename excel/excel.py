import os
from datetime import datetime, timedelta
from typing import List

import openpyxl
from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.styles import Font
from openpyxl.worksheet.worksheet import Worksheet


class ExcelHandler:
    def __init__(self, input_file_path: str, input_sheet_name: str = "input", models_start_cell: tuple = (1, 3), models_end_cell: tuple = (2, 100)):
        self.file = input_file_path
        self.workbook

        self.models_start_cell = models_start_cell
        self.models_end_cell = models_end_cell

        self.input_sheet_name = input_sheet_name
        self._check_input_sheet()

    def _check_input_sheet(self):
        if self.input_sheet_name not in self.workbook.sheetnames:
            raise ValueError(f"Input sheet \"{self.input_sheet_name}\" not found!")

    @property
    def workbook(self) -> Workbook:
        return openpyxl.load_workbook(self.file)

    @property
    def input_sheet(self) -> Worksheet:
        return self.workbook[self.input_sheet_name]

    def save(self, workbook: Workbook) -> None:
        try:
            workbook.save(self.file)
        except PermissionError:
            print(f'Закройте файл {self.file}')

    def get_models(self) -> dict[str: int]:
        sheet = self.input_sheet

        models_rows = map(lambda row: (row[0], 0 if row[1] is None else row[1]),
                                       filter(lambda row: row[0] is not None,
                                              sheet.iter_rows(min_col=self.models_start_cell[0],
                                                              min_row=self.models_start_cell[1],
                                                              max_col=self.models_end_cell[0],
                                                              max_row=self.models_end_cell[1],
                                                              values_only=True)
                                              )
                                       )

        return dict(models_rows)

# def load(products: List[Product], filename: str):
#     output = []
#
#     delete_default_sheet = False
#     try:
#         workbook = openpyxl.load_workbook(filename)
#     except:
#         workbook = openpyxl.Workbook()
#         delete_default_sheet = True
#
#     sheet_name = str(datetime.now().date())
#     if sheet_name not in workbook.sheetnames:
#         sheet = workbook.create_sheet(sheet_name)
#
#         if delete_default_sheet:
#             del workbook["Sheet"]
#
#         # Titles
#         titles = ["Имя", "Артикул", "Цена", "Наличие"]
#         for index, title in enumerate(titles):
#             cell = sheet.cell(1, index + 1, title)
#             cell.font = Font(bold=True)
#     else:
#         sheet = workbook[sheet_name]
#
#     # Getting previous products
#     previous_sheet_name = str(datetime.now().date() - timedelta(days=1))
#     previous_products = []
#     if previous_sheet_name in workbook.sheetnames:
#         previous_sheet: Worksheet = workbook[previous_sheet_name]
#         for index in range(2, previous_sheet.max_row + 1):
#             cells_range: List[List[Cell]] = previous_sheet[f"A{index}:D{index}"]
#             for cells in cells_range:
#                 data = list(map(lambda cell: cell.value, cells))
#                 product = Product(data[0], data[1], data[2], data[3] == "Есть")
#                 previous_products.append(product)
#
#     # Products
#     for index, product in enumerate(products):
#         previous_product = list(filter(lambda previous_product: previous_product.article == product.article, previous_products))
#         if previous_product:
#             previous_product = previous_product[0]
#             if previous_product.in_stock is False and product.in_stock is True:
#                 output.append(f"{product} теперь в наличии по цене {product.price} ₽")
#             if previous_product.price != product.price:
#                 output.append(f"Цена товара {product} изменилась: {previous_product.price} ₽ -> {product.price} ₽")
#
#         sheet.cell(index + 2, 1, product.name)
#         sheet.cell(index + 2, 2, product.article)
#         sheet.cell(index + 2, 3, product.price)
#         sheet.cell(index + 2, 4, "Есть" if product.in_stock else "Нет")
#
#     # Previous products
#     for index, product in enumerate(previous_products):
#         if list(filter(lambda new_product: new_product.article == product.article, products)): continue
#
#         sheet.cell(index + 2, 1, product.name)
#         sheet.cell(index + 2, 2, product.article)
#         sheet.cell(index + 2, 3, product.price)
#         sheet.cell(index + 2, 4, "Нет")
#
#     try:
#         workbook.save(filename)
#     except PermissionError:
#         print(f"Закройте таблицу \"{filename}\"")
#
#     return output
