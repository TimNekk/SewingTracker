import logging
import re
from typing import List

from headers_converter import headers_converter

from parsing.websites import Parser


class Citilink(Parser):
    def __init__(self):
        self._price_selector = ".ProductHeader__price-default"
        self._base_url = "https://www.citilink.ru"
        self._search_url = self._base_url + "/search/?text="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}

        # pcl может устареть
        headers = headers_converter.convert("""cookie: _pcl=eW5h9RmFCqvDcg==;""")
        soup = self._get_soup(url + f"&menu_id=466", headers=headers)

        models_grid = soup.select(".ProductCardVertical__name")
        if not models_grid:
            return models

        for model in models_grid:
            try:
                model_name = model.text
                model_url = self._base_url + model['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

