import re
from typing import Optional

from fuzzywuzzy import fuzz

from parsing.websites import Parser


class DamaDomaParser(Parser):
    def __init__(self):
        self._price_selector = ".info_item .middle_info .prices .price"
        self._base_url = "https://damadoma.ru"
        self._search_url = self._base_url + "/index.php?searchstring="

    def parse_model(self, url: str) -> Optional[int]:
        soup = self._get_soup(url)
        if "Нет информации в базе по наличию товара." not in map(lambda item: item.text, soup.find_all("font", color="red")):
            price = int(re.findall(r"\d+", soup.find("font", id="currentPrice").text.replace(",", ""))[0])
            return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_grid = soup.select(".cat")
        if not models_grid:
            return

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text.split("[")[0]).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = self._base_url + "/" + model['href']
                    models[model_name] = model_url
            except Exception:
                pass

        return models

