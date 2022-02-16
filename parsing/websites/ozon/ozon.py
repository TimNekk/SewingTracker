import re
from typing import Optional

from fuzzywuzzy import fuzz

from parsing.websites import Parser


class OzonParser(Parser):
    def __init__(self):
        self._price_selector = "#layoutPage > div.f5z > div.container.f6z > div.jl.lj4 > div.jl.lj5.lj2.l2j > div.jl.lj5.lj2.jl3 > div > div > div > div:nth-child(1) > div > div > div.jq9.rj0.r1j > div > span.q9j.jr > span"
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

        models_grid = soup.select("#layoutPage > div.f5z > div:nth-child(8) > div > div > div:nth-child(2) > div.ho9 > div > div > div > div:nth-child(1) > div.m8h > a")

        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text.split("[")[0]).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = self._base_url + model['href']
                    models[model_name] = model_url
            except Exception:
                pass

        return models