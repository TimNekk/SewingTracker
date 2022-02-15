import re
from typing import Optional

from parsing.websites import Parser


class SewingAdvisorParser(Parser):
    def __init__(self):
        self._price_selector = ".payment__price"
        self._search_url = "https://sewingadvisor.ru/search/?category=product&search="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".item")
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name_a = model.select_one(".item__title")
                model_name = model_name_a.text
                model_url = model_name_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

