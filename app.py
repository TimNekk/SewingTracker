import logging
import time
from pprint import pprint
from time import sleep
import sys
from typing import Optional, List

import schedule

from classes import Model
from loader import db, ph
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
            logging.info(f"{index+1}/{len(models)} Exporting model \"{model.name}\"...")

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
    def update_models(market: Optional[str] = None) -> None:
        logging.info("Updating models...")

        models = db.get_models()
        for index, model in enumerate(models):
            logging.info(f"{index+1}/{len(models)} Updating model \"{model.name}\"")
            model.update_prices(market)

    def export_models_from_excel_to_db(self):
        # 1 есть в таблице, есть в дб (ничего)
        # 2 есть в таблице, нет в дб (добавляем)
        # 3 нет в таблице, есть в дб (убираем)
        db_models = list(map(lambda model: model.name, db.get_models()))
        excel_models = self.excel.get_models().items()

        for excel_name, excel_price in excel_models:
            if excel_name in db_models:
                db_models.remove(excel_name)
            else:
                db.add_model(excel_name, excel_price)
                logging.info(f"Model \"{excel_name}\" added to db")

        # Убираем те, которых нет в таблице
        for model in db_models:
            db.remove_model(model)
            logging.info(f"Model \"{model}\" removed from db")

    def add_model(self, model_name: str) -> Model:
        model = db.add_model(model_name)
        logging.info(f"{model_name} added to db")
        self.excel.add_model(model_name)
        self.excel.save()
        logging.info(f"{model_name} added to excel")
        return model

    def parse_models_from_markets(self):
        # Merrylock 007/3000
        # Merrylock 007 / 3000
        self.parse_model_from_market("sewing-kingdom", "merrylock")
        self.parse_model_from_market("sewing-kingdom", "necchi")
        self.parse_model_from_market("textiletorg", "merrylock")

    def parse_model_from_market(self, market_name: str, search: str) -> None:
        models = ph.parse_search(market_name, search)

        for model_name, model_url in models.items():
            is_new, name = db.get_real_model_name(model_name)
            logging.info(f"Вывод: {f'Новая модель ({name})' if is_new else f'Уже есть ({name})'}")

            if is_new:
                model = self.add_model(name)
                model.set_url(market_name, model_url)

    def update(self):
        try:
            self.export_models_from_excel_to_db()
            self.parse_models_from_markets()
            self.update_models()
            self.export_prices_form_db_to_excel()
            logging.info("\nГОТОВО! Можно открывать EXCEL\n")
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    args = dict(map(lambda arg: tuple(arg.split("=")), sys.argv[1:]))
    mode = args.get("mode")
    logging.info(f"Started with params {args}")

    app = App(input_path, open_model_history_path)

    if mode == "update":
        app.update()
        schedule.every().hour.at(":00").do(app.update)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif mode == "update_model":
        app.update_models(args.get("market"))
        app.export_prices_form_db_to_excel()
    elif mode == "model":
        app.excel.create_temp_model_file(db.get_model(args.get("model")), args.get("market"))
    elif mode == "add_market":
        db.add_market(input("Введите название магазина: "))

