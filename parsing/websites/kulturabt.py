import logging
import re
from typing import List

from parsing.websites import Parser


class KulturabtParser(Parser):
    def __init__(self):
        self._price_selector = ".product-new .b-v2-product-inner-cart__actual-price"
        self._base_url = "https://moskva.kulturabt.ru"
        self._search_url = self._base_url + "/catalog/?q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select_one(".b-v2-catalog-items__list")
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name_a = model.select_one(".b-v2-catalog-product__title-link")
                model_name = model_name_a.text
                model_url = self._base_url + model_name_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

