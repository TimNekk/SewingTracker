import re
from typing import Optional

from parsing.websites import Parser


class VeritazParser(Parser):
    def __init__(self):
        self._base_url = "https://www.veritaz.ru"
        self._search_url = self._base_url + "/index.php?x=0&y=0&searchstring="

    def parse_model(self, url: str) -> Optional[int]:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.find("font", id="currentPrice").text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_a = soup.find_all("a", class_="cat")

        for model_a in models_a:
            try:
                model_name = model_a.text
                model_url = self._base_url + "/" + model_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

