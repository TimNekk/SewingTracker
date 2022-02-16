import re
from typing import Optional

from parsing.websites import Parser


class BeCompactParser(Parser):
    def __init__(self):
        self._price_selector = ".product-price__new"
        self._base_url = "https://becompact.ru"
        self._search_url = self._base_url + "/personal/search/full"

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        models = {}

        response = self._send_post_request(self._search_url + "category=&p%5Bs%5D=0&p%5Bcv%5D=0&q=merrylock&f=1")
        print(response.content)

        soup = 1
        models_grid = soup.find_all("div", class_="block-product-card block-product-card_minsize")
        print(models_grid)
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name_a = model.select_one(".link-nostyle")
                model_name = model_name_a.text
                model_url = self._base_url + model_name_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

