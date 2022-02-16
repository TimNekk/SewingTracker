import re
from typing import Optional

from parsing.websites import Parser


class JustParser(Parser):
    def __init__(self):
        self._price_selector = ".price-abbr"
        self._base_url = "https://just.ru"
        self._search_url = self._base_url + "/search/?s="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".product")
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name_a = model.select_one(".catalog-content .catalog-detail-list .product .internal .description a.title")
                model_name = model_name_a.text
                model_url = self._base_url + model_name_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

