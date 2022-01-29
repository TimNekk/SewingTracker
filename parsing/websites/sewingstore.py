import logging
import re
from typing import List

from parsing.websites import Parser


class SewingStoreParser(Parser):
    def __init__(self):
        self._price_selector = "#product h2.price, #product div.price, #product_view h2.price"
        self._search_url = "https://www.sewingstore.ru/search/?search="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".product-thumb .h4 a")
        if not models_grid:
            return models

        for model in models_grid:
            try:
                model_name = model.text
                model_url = model['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

