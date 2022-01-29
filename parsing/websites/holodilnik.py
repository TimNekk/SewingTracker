import re

from parsing.websites import Parser
from fuzzywuzzy import fuzz


class HolodilnikParser(Parser):
    def __init__(self):
        self._price_selector = ".region_block .prc_val span.big"
        self._base_url = "https://www.holodilnik.ru"
        self._search_url = "https://autocomplete.diginetica.net/autocomplete?st="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(soup.select_one(self._price_selector).text.replace(" ", ""))
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}
        response = self._send_get_request(url + "&apiKey=BZQ1NIP98I").json()
        models_grid = response.get("products")

        if not models_grid:
            return models

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.get("name")).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = self._base_url + model.get("link_url")
                    models[model_name] = model_url
            except Exception:
                pass

        return models