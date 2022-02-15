import re
from typing import Optional

from parsing.websites import Parser


class OzonParser(Parser):
    def __init__(self):
        self._price_selector = ".jm9 .m9j"
        self._base_url = "https://ozon.com"
        self._search_url = self._base_url + "/search/?from_global=true&text="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", "").replace(" ", ""))[0])
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".gz7")

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