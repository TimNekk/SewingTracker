from loader import db
from data.config import input_path
from excel.excel import ExcelHandler


class App:
    def __init__(self, excel_input_path: str):
        self.excel = ExcelHandler(excel_input_path)

    def export_prices_form_db_to_excel(self) -> None:
        for model in db.get_models():
            for market in db.markets:
                try:
                    price = model.get_market_price(market)
                except ValueError as e:
                    print(e)
                    continue
                self.excel.edit_model_market_cell(model_name=model.name, market_name=market, value=price)

    @staticmethod
    def update_models() -> None:
        for model in db.get_models():
            model.update_prices()

    def export_models_from_excel_to_db(self) -> None:
        for name, price in self.excel.get_models().items():
            try:
                db.add_model(name, price)
            except ValueError as e:
                print(e)


if __name__ == '__main__':
    app = App(input_path)
    # excel = ExcelHandler(input_path)
    # print(excel.save(excel.workbook))
    app.export_prices_form_db_to_excel()


    # excel = ExcelHandler(input_path)
    # try:
    #     model = db.get_model("Merrylock 220")
    #     excel.edit_model_market_cell(model.name, list(model.markets.keys())[0], "test")
    # except ValueError as e:
    #     print(e)

# TODO: Узнать, нужно ли брать цену которой нет на сайте

# def update_products():
#     products = get_products_from_sewing_kingdom()
#     print(3)
#     output = load(products, 'Продукты.xlsx')
#     if output:
#         email = EmailSender(Email.sender, Email.password)
#         email.send(email=Email.receiver,
#                    text="\n".join(output),
#                    title=f"Отчет по \"Швейное королевство\" ({datetime.now().date()})")
#
#
# if __name__ == '__main__':
#     update_products()
#
#     schedule.every().day.do(update_products)
#
#     while True:
#         schedule.run_pending()
#         sleep(60)
