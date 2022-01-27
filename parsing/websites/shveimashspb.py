import logging
import re

from parsing.websites import Parser


class ShveiMashSpbParser(Parser):
    def __init__(self):
        self._price_selector = "#catalog_element .wrapper_price .price"
        self._base_url = "https://shveimash.spb.ru"
        self._search_url = self._base_url + "/catalog/?q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        # ПРАРСИТ ТОЛЬКО ПЕРВУЮ СТРАНИЦУ!!!

        url = self._search_url + search.replace(" ", "+")
        models = {}
        page = 1

        while True:
            soup = self._get_soup(url + f"&PAGEN_3={page}")

            models_grid = soup.select("#catalog_grid .item")

            for model in models_grid:
                try:
                    model_name_a = model.select_one("#catalog_grid .item .header .name")
                    model_name = model_name_a.text
                    model_url = self._base_url + model_name_a['href']
                    models[model_name] = model_url
                except Exception as e:
                    logging.error(e)

            break

        return models