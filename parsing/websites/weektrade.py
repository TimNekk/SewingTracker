import re
from typing import Optional

from parsing.websites import Parser


class WeekTradeParser(Parser):
    def __init__(self):
        self._price_selector = ".price"
        self._base_url = "https://weektrade.ru"
        self._search_url = self._base_url + "/cat/?searchstring="

    def parse_model(self, url: str) -> Optional[int]:
        soup = self._get_soup(url)
        if soup.find("span", style="font-size:12px").text.strip() != "Товара нет в наличии":
            price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
            return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        soup = self._get_soup(url)

        models_a = soup.find_all("a", class_="b1c-name")

        for model_a in models_a:
            try:
                model_name = model_a.text
                model_url = self._base_url + model_a['href']
                models[model_name] = model_url
            except Exception:
                pass

        return models

