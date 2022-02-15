import re
from typing import Optional

from parsing.websites import Parser


class ElecityParser(Parser):
    def __init__(self):
        self._price_selector = ".catalog_item_cur_left"
        self._base_url = "https://elecity.ru"
        self._search_url = self._base_url + "/search/?q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).find_all("div")[-1].text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".catalog_index_block_item")
        empty_search_page = soup.select_one(".empty_search_page")
        if not models_grid or empty_search_page:
            return

        for model in models_grid:
            try:
                if model.select_one(".catalog_item_nalichie").text == "Нет в наличии":
                    continue
                model_name_a = model.select_one(".catalog_item_name a")
                model_name = model_name_a.text
                model_url = self._base_url + model_name_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

