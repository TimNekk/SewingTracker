import logging

from classes import ModelHistory, HistoryPoint


class Model:
    def __init__(self, id: int, name: str, price: int, *args):
        self.id = id
        self.name = name
        self.price = price

        self.markets = {}
        self._set_markets(*args)

    def __str__(self):
        return f"Model \"{self.name}\""

    def _set_markets(self, *args) -> None:
        from loader import db
        self.markets = {name: url for name, url in zip(db.markets, args)}

    def get_history(self) -> ModelHistory:
        from loader import db
        sql = f"SELECT * FROM \"{self.name}\""
        data = db.execute(sql, fetchall=True)
        return ModelHistory(self.name, list(map(lambda history_point_data: HistoryPoint(self.name, *history_point_data), data)))

    def set_price(self, amount: int) -> None:
        self._update("price", amount)

    def update_prices(self) -> None:
        history = self.get_history()
        history.create_new_history_point()

        from loader import ph
        for market_name, model_url in self.markets.items():
            if model_url is None:
                logging.warning(f"Url for model \"{self.name}\" for market \"{market_name}\" not found")
                continue

            try:
                price = ph.parse(market_name, model_url)
            except Exception as e:
                logging.error(e)
                continue
            history.update_last_history_point(market_name, price)

    def get_market_price(self, market_name: str, history: ModelHistory) -> int:
        return history.latest_point.prices.get(market_name)

    def add_market(self, market_name: str) -> None:
        self._modify_market(market_name, add=True)

    def remove_market(self, market_name: str) -> None:
        self._modify_market(market_name, add=False)

    def _modify_market(self, market_name: str, add: bool) -> None:
        from loader import db
        sql = f"ALTER TABLE \"{self.name}\" {'ADD' if add else 'DROP'} COLUMN \"{market_name}\" {'INT' if add else ''}"
        db.execute(sql, commit=True)

    def _update(self, parameter, value) -> None:
        from loader import db
        sql = f"UPDATE models SET {parameter} = {value} WHERE id = {self.id}"
        db.execute(sql, commit=True)
