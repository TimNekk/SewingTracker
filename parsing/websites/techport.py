import logging
import re
from typing import List, Optional

from fuzzywuzzy import fuzz

from parsing.websites import Parser


class TechPortParser(Parser):
    def __init__(self):
        self._price_selector = ".tcp-product-body__new-price"
        self._base_url = "https://www.techport.ru"
        self._search_url = self._base_url + "/q/?catid=20000&t="

    def parse_model(self, url: str) -> Optional[int]:
        soup = self._get_soup(url)
        if soup.select_one(".tcp-list-group__link_dot").text == "Нет в наличии": return
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select("#catalog_list .tcp-product-body__title a")

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

