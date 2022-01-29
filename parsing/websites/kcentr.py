import logging
import re
from typing import List

from fuzzywuzzy import fuzz

from parsing.websites import Parser


class KcentrParser(Parser):
    def __init__(self):
        self._price_selector = ".card-related__main-price"
        self._base_url = "https://kcentr.ru"
        self._search_url = self._base_url + "/search/400/?q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".product-name")

        if not models_grid:
            return models

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = self._base_url + model['href']
                    models[model_name] = model_url
            except Exception:
                pass

        return models

