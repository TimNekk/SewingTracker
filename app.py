import logging
import time
import sys
from datetime import datetime
from pprint import pprint
from typing import Optional, Dict, Tuple, List

import schedule
from oauth2client.service_account import ServiceAccountCredentials

from classes import Model
from loader import db, ph
from data.config import credentials
from sheets.sheets import Sheets


class App:
    def __init__(self, credentials: ServiceAccountCredentials):
        self.sheets = Sheets(credentials)
        logging.info("App Initialized")

    def export_prices_form_db_to_sheets(self):
        self.sheets.clear_sheet()
        cells = self.sheets.get_cells()
        markets = self.sheets.get_markets_column(cells)
        models = self.sheets.get_models_column(cells)
        wrong_prices = {}
        logging.info("Exporting prices form db to sheets")

        db_models = db.get_models()
        for model in db_models:
            logging.info(f"Exporting model \"{model.name}\"...")

            for market in db.markets:
                history = model.get_history()
                try:
                    price = history.latest_point.prices.get(market)
                except ValueError as e:
                    logging.error(e)
                    continue

                if price is not None:
                    cells[models.index(model.name)][markets.index(market)] = price

                    # Уведомление
                    try:
                        mrc = int(cells[models.index(model.name)][1])
                    except ValueError:
                        continue

                    if price < mrc:
                        if not wrong_prices.get(market):
                            wrong_prices[market] = []
                        wrong_prices[market].append((model.name, mrc, price))

        cells[0][0] = f"Обновлено: {datetime.now()}"
        self.sheets.update_cells(cells)
        return wrong_prices

    @staticmethod
    def update_models(market: Optional[str] = None) -> None:
        logging.info("Updating models...")

        models = db.get_models()
        for index, model in enumerate(models):
            logging.info(f"{index+1}/{len(models)} Updating model \"{model.name}\"")
            model.update_prices(market)

    def export_models_from_sheets_to_db(self) -> None:
        # 1 есть в таблице, есть в дб (ничего)
        # 2 есть в таблице, нет в дб (добавляем)
        # 3 нет в таблице, есть в дб (убираем)
        db_models = list(map(lambda model: model.name, db.get_models()))

        for model in self.sheets.get_models():
            if model in db_models:
                db_models.remove(model)
            else:
                db.add_model(model, 0)
                logging.info(f"Model \"{model}\" added to db")

        # Убираем те, которых нет в таблице
        for model in db_models:
            db.remove_model(model)
            logging.info(f"Model \"{model}\" removed from db")

    def add_model(self, model_name: str) -> Model:
        model = db.add_model(model_name)
        logging.info(f"{model_name} added to db")
        self.sheets.add_model(model_name)
        logging.info(f"{model_name} added to sheets")
        return model

    def parse_models_from_markets(self) -> None:
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

    @staticmethod
    def notify(wrong_prices: dict):
        if not wrong_prices:
            return

        text = "<b>Список цен, ниже чем МРЦ</b>\n"

        for index, (market, data) in enumerate(wrong_prices.items()):
            text += f"\n{index + 1}) Магазин <b>{market}</b>\n"
            for (model, mrc, price) in data:
                text += f"▶ Модель <b>{model}</b>: {price}р (МРЦ: {mrc}р)\n"

        with open("data/notify.txt", 'w') as file:
            file.write(text)

    def update(self):
        try:
            self.export_models_from_sheets_to_db()
            self.parse_models_from_markets()
            self.update_models()
            wrong_prices = self.export_prices_form_db_to_sheets()
            self.notify(wrong_prices)
            logging.info("\nГОТОВО!\n")
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    args = dict(map(lambda arg: tuple(arg.split("=")), sys.argv[1:]))
    mode = args.get("mode")
    logging.info(f"Started with params {args}")

    app = App(credentials)

    if mode == "update":
        app.update()
        schedule.every(3).hours.do(app.update)
        # schedule.every().day.at("06:00").do(app.update)
        # schedule.every().day.at("13:00").do(app.update)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif mode == "update_model":
        app.update_models(args.get("market"))
        app.export_prices_form_db_to_sheets()
    elif mode == "model":
        app.sheets.create_temp_model_file(db.get_model(args.get("model")), args.get("market"))
    elif mode == "add_market":
        db.add_market(input("Введите название магазина: "))
    # else:
        # print(ph.parse_model("kulturabt", "https://moskva.kulturabt.ru/catalog/shveynoe_oborudovanie/koverlok/merrylock_0115a/"))
        # pprint(ph.parse_search("kulturabt", "merrylock"))
        # app.update_models("kcentr")
        # a = app.export_prices_form_db_to_sheets()
        # app.notify(a)

