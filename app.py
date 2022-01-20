import logging
import sys

from loader import db
from data.config import input_path, open_model_history_path
from excel.excel import ExcelHandler


class App:
    def __init__(self, excel_input_path: str, open_model_history_file: str):
        self.excel = ExcelHandler(excel_input_path, open_model_history_file)
        logging.info("App Initialized")

    def export_prices_form_db_to_excel(self) -> None:
        logging.info("Exporting prices form db to excel")

        models = db.get_models()
        for index, model in enumerate(models):
            logging.info(f"{index}/{len(models)} Exporting model \"{model.name}\"...")

            for market in db.markets:
                history = model.get_history()
                try:
                    price = history.latest_point.prices.get(market)
                except ValueError as e:
                    logging.error(e)
                    continue

                if price is not None:
                    self.excel.edit_model_market_cell(model_name=model.name, market_name=market, value=price)

        self.excel.save()

    @staticmethod
    def update_models() -> None:
        logging.info("Updating models...")

        models = tuple(filter(lambda model: model.has_markets, db.get_models()))
        for index, model in enumerate(models):
            logging.info(f"{index+1}/{len(models)} Updating model \"{model.name}\"")
            model.update_prices()

    def export_models_from_excel_to_db(self) -> None:
        for name, price in self.excel.get_models().items():
            try:
                db.add_model(name, price)
            except ValueError as e:
                logging.error(e)


if __name__ == '__main__':
    args = dict(map(lambda arg: tuple(arg.split("=")), sys.argv[1:]))
    mode = args.get("mode")
    logging.info(f"Started with params {args}")

    app = App(input_path, open_model_history_path)

    if mode == "update":
        app.update_models()
        app.export_prices_form_db_to_excel()
    elif mode == "model":
        app.excel.create_temp_model_file(db.get_model(args.get("model")), args.get("market"))
    elif mode == "add_market":
        db.add_market(input("Введите название магазина: "))
    else:
        from parsing.parsers_handler import ParsersHandler
        print(ParsersHandler().parse("wildberries", "https://www.wildberries.ru/catalog/18507637/detail.aspx"))

    # excel = ExcelHandler(input_path)
    # try:
    #     model = db.get_model("Merrylock 220")
    #     excel.edit_model_market_cell(model.name, list(model.markets.keys())[0], "test")
    # except ValueError as e:
    #     print(e)

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
