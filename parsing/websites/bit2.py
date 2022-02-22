import re
from typing import Optional

from fuzzywuzzy import fuzz

from parsing.websites import Parser


class Bit2Parser(Parser):
    def __init__(self):
        self._price_selector = ".__blue"
        self._base_url = "https://2bit.ru"
        self._search_url = self._base_url + "/search/?q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        if not soup.select_one(".product__buy__on__page .product__available").text:
            return
        price = int("".join(re.findall(r"\d+", soup.select(self._price_selector)[1].text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".section__S")
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name_a = model.find_all("a", class_="__black")[1]
                model_name = re.sub(r"[а-яА-Я]+", "", model_name_a.text.replace("\r\n", "").strip()).strip()
                if fuzz.ratio(model_name, search) >= 96:
                    model_url = self._base_url + model_name_a['href']
                    models[model_name] = model_url
            except Exception:
                pass

        return models

