from datetime import datetime


class HistoryPoint:
    def __init__(self, model_name: str, date: str, *args):
        self.model_name = model_name
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        self.prices: dict
        self._set_markets(*args)

    def _set_markets(self, *args) -> None:
        from loader import db
        self.prices = {name: url for name, url in zip(db.markets, args)}

    def update(self, market_name: str, price: int) -> None:
        from loader import db
        sql = f"UPDATE \"{self.model_name}\" SET \"{market_name}\" = {price} WHERE date = \"{self.date}\""
        db.execute(sql, commit=True)
