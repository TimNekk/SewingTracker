import logging
import re
from typing import List

from parsing.websites import Parser


class SewingKingdomParser(Parser):
    def __init__(self):
        self._price_selector = ".pmip_buy_price"
        self._search_url = "https://sewing-kingdom.ru/index.php?route=product/search&search="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text)[0])
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}
        page = 1

        while True:
            soup = self._get_soup(url + f"&page={page}")

            models_grid = soup.find("div", class_="product-list")
            if not models_grid:
                break

            for model in models_grid:
                try:
                    model_name_a = model.find("div", class_="name").find("a")
                    model_name = model_name_a.text
                    model_url = model_name_a['href']
                    models[model_name] = model_url
                except Exception:
                    pass

            page += 1

        return models

