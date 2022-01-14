import logging
import sqlite3
from typing import Optional, List

from classes import Model


class Database:
    def __init__(self, path_to_db='data/main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        print(self.path_to_db)
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = tuple(), fetchone=False,
                fetchall=False, commit=False):

        connection = self.connection
        connection.set_trace_callback(self.log)
        cursor = connection.cursor()

        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        data = None
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def does_table_exist(self, table: str) -> bool:
        sql = f"PRAGMA table_info({table})"
        return self.execute(sql, fetchone=True)

    @staticmethod
    def log(statement):
        logging.debug(statement)

    def get_models(self) -> List[Model]:
        sql = "SELECT * FROM models"
        data = self.execute(sql, fetchall=True)
        return list(map(lambda model_data: Model(*model_data), data))

    def get_model(self, name: Optional[str] = None, id: Optional[int] = None) -> Model:
        if id is not None:
            sql = f"SELECT * FROM models WHERE id={id}"
        elif name is not None:
            sql = f"SELECT * FROM models WHERE name=\"{name}\""
        else:
            raise ValueError("Model id and name was not passed")

        data = self.execute(sql, fetchone=True)
        return Model(*data)

    def get_models_names(self) -> List[str]:
        return list(map(lambda model: model.name, self.get_models()))

    @property
    def markets(self) -> List[str]:
        sql = f"SELECT name FROM PRAGMA_TABLE_INFO('models')"
        data = self.execute(sql, fetchall=True)
        return list(map(lambda name: name[0], data[3:]))

    def _get_tables_names(self) -> List[str]:
        sql = f"SELECT name FROM sqlite_master WHERE type='table';"
        data = self.execute(sql, fetchall=True)
        return list(map(lambda name: name[0], data))

    def add_market(self, name: str):
        if name in self.markets:
            raise ValueError(f"Market \"{name}\" already exists")

        sql = f"ALTER TABLE models ADD COLUMN \"{name}\" STRING"
        self.execute(sql, commit=True)

        for model in self.get_models():
            model.add_market(name)

    def remove_market(self, name):
        if name not in self.markets:
            raise ValueError(f"Market \"{name}\" does not exist")

        sql = f"ALTER TABLE models DROP COLUMN \"{name}\""
        self.execute(sql, commit=True)

        for model in self.get_models():
            model.remove_market(name)

    def add_model(self, name, price):
        if name in self.get_models_names():
            raise ValueError(f"Model \"{name}\" already exists")

        sql = f"INSERT INTO models (name, price) VALUES (\"{name}\", {price})"
        self.execute(sql, commit=True)

        sql = f"CREATE TABLE [{name}] (date DATETIME DEFAULT (date('now', 'localtime') ) NOT NULL)"
        self.execute(sql, commit=True)

        model = self.get_model(name)
        for market in self.markets:
            model.add_market(market)
