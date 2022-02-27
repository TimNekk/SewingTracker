from enum import Enum


class Status(Enum):
    exporting_to_db = "Выгрузка моделей из таблиц"
    parsing_market = "Поиск моделей в магазине"
    parsing_model = "Парсинг модели"
    exporting_to_sheets = "Загрузка цен в таблицу"
    done = "Загрузка завершена"
