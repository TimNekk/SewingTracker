from classes import ModelHistory, HistoryPoint


class Model:
    def __init__(self, id: int, name: str, price: int, *args):
        self.id = id
        self.name = name
        self.price = price

        self.markets = {}
        self._set_markets(*args)

    def _set_markets(self, *args) -> None:
        from loader import db
        self.markets = {name: url for name, url in zip(db.markets, args)}

    def _get_history(self) -> ModelHistory:
        from loader import db
        sql = f"SELECT * FROM \"{self.name}\""
        data = db.execute(sql, fetchall=True)
        return ModelHistory(self.name, list(map(lambda history_point_data: HistoryPoint(self.name, *history_point_data), data)))

    def set_price(self, amount: int) -> None:
        self._update("price", amount)

    def update_prices(self) -> None:
        history = self._get_history()
        history.create_new_history_point()

        from loader import ph
        for market_name, model_url in self.markets.items():
            try:
                price = ph.parse(market_name, model_url)
            except Exception as e:
                print(e)
                continue

            history.update_last_history_point(market_name, price)

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
