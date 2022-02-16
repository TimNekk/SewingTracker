import re
from typing import Optional

from parsing.websites import Parser


class SkyeyParser(Parser):
    def __init__(self):
        self._price_selector = ".info_item .middle_info .prices .price"
        self._base_url = "https://skyey.ru"
        self._search_url = self._base_url + "/catalog/?s=Найти&q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".catalog_item .item-title a, .view-item .item-title a span")
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name = model.text
                model_url = self._base_url + model['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

