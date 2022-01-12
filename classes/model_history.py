from typing import List

from classes.history_point import HistoryPoint


class ModelHistory:
    def __init__(self, model_name: str, history_points: List[HistoryPoint]):
        self.model_name = model_name
        self.points = history_points

    def create_new_history_point(self) -> None:
        from loader import db
        sql = f"INSERT INTO \"{self.model_name}\" (date) VALUES (datetime('now', 'localtime'))"
        db.execute(sql, commit=True)

        point = self._get_last_history_point()
        self.points.append(point)

    def _get_last_history_point(self) -> HistoryPoint:
        from loader import db
        sql = f"SELECT * FROM \"{self.model_name}\" ORDER BY date DESC LIMIT 1"
        history_point_data = db.execute(sql, fetchone=True)
        return HistoryPoint(self.model_name, *history_point_data)

    def update_last_history_point(self, market_name: str, price: int) -> None:
        point = self.points[-1]
        point.update(market_name, price)
