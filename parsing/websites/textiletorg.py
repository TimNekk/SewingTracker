import logging
import re

from parsing.websites import Parser


class TextiletorgParser(Parser):
    def __init__(self):
        self._base_url = "https://www.textiletorg.ru"
        self._search_url = self._base_url + "/search/?QUERY="
        self._price_selector = "#item .right_block_cart .price-price"

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(soup.select_one(self._price_selector).text.replace(" ", ""))
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search.replace(" ", "+")
        models = {}
        page = 1

        while True:
            soup = self._get_soup(url + f"&PAGEN_1={page}")

            models_grid = soup.select(".grid-list .itemlist .item")

            for model in models_grid:
                try:
                    model_name_a = model.select_one(".itemlist .n_catalog_name a")
                    model_name = model_name_a.text
                    model_url = self._base_url + model_name_a['href']
                    models[model_name] = model_url
                except Exception:
                    pass

            next_button = list(filter(lambda el: "Вперед >" in el, soup.select(".ajax-pagination .pagination .pager__button")))
            if next_button:
                page += 1
            else:
                break

        return models