import logging
import time
import sys
from datetime import datetime
from typing import Optional

import schedule
from oauth2client.service_account import ServiceAccountCredentials

from classes import Model
from loader import db, ph
from data.config import credentials
from sheets import Status
from sheets.sheets import Sheets


class App:
    def __init__(self, credentials: ServiceAccountCredentials):
        self.sheets = Sheets(credentials)
        logging.info("App Initialized")

    def export_prices_form_db_to_sheets(self):
        self.sheets.set_status(Status.exporting_to_sheets)

        cells = self.sheets.get_cells(clear=True)
        markets = list(map(str, self.sheets.get_markets_column(cells)))
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
                    try:
                        cells[models.index(model.name)][markets.index(market)] = f"=ГИПЕРССЫЛКА(\"{model.markets.get(market)}\"; {price})"
                    except Exception as e:
                        logging.error(e)

                    # Уведомление
                    try:
                        mrc = int(cells[models.index(model.name)][1])
                    except ValueError:
                        continue

                    if price < mrc:
                        if not wrong_prices.get(market):
                            wrong_prices[market] = []
                        wrong_prices[market].append((model.name, mrc, price))

        self.sheets.update_cells(cells)
        return wrong_prices

    def update_models(self, market: Optional[str] = None) -> None:
        logging.info("Updating models...")

        models = db.get_models()
        for index, model in enumerate(models):
            logging.info(f"{index+1}/{len(models)} Updating model \"{model.name}\"")
            self.sheets.set_status(Status.parsing_model, model.name)
            model.update_prices(market)

    def export_models_from_sheets_to_db(self) -> None:
        self.sheets.set_status(Status.exporting_to_db)

        db_models = list(map(lambda m: m.name, db.get_models()))

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
        self.parse_models_from_market("sewing-kingdom", "merrylock")
        self.parse_models_from_market("sewing-kingdom", "necchi")
        self.parse_models_from_market("textiletorg", "merrylock")

    def parse_models_from_market(self, market_name: str, search: str) -> None:
        self.sheets.set_status(Status.parsing_market, market_name)

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
                text += f"- Модель <b>{model}</b>: {price}р (МРЦ: {mrc}р)\n"

        with open("data/notify.txt", 'w') as file:
            file.write(text)

    @staticmethod
    def add_missing_markets_to_db():
        logging.info("Adding missing markets to DB...")
        markets = ph.parsers.keys()
        markets_db = db.markets
        for market in markets:
            if market not in markets_db:
                logging.info(f"{market} added to DB")
                db.add_market(market)
        logging.info("Done!")

    def update(self):
        try:
            self.export_models_from_sheets_to_db()
            self.parse_models_from_markets()
            self.update_models()
            wrong_prices = self.export_prices_form_db_to_sheets()
            self.notify(wrong_prices)
            self.sheets.set_status(Status.done)

        except Exception as e:
            logging.error(e)

        logging.info("\nГОТОВО!\n")


if __name__ == '__main__':
    args = dict(map(lambda arg: tuple(arg.split("=")), sys.argv[1:]))
    mode = args.get("mode")
    logging.info(f"Started with params {args}")

    app = App(credentials)

    if mode == "update":
        app.add_missing_markets_to_db()
        app.update()
        schedule.every(3).hours.do(app.update)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif mode == "update_model":
        app.update_models(args.get("market"))
        app.export_prices_form_db_to_sheets()
    # elif mode == "model":
    #     app.sheets.create_temp_model_file(db.get_model(args.get("model")), args.get("market"))
    elif mode == "add_market":
        db.add_market(input("Введите название магазина: "))
    else:
        print(ph.parse_model("mvideo", "https://www.mvideo.ru/products/overlok-merrylock-0055-50115390"))
        # pprint(ph.parse_search("ozon-shveyberi", "merrylock"))

