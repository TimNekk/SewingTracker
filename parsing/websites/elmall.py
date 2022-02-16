import re
from typing import Optional

from parsing.websites import Parser


class ElMallParser(Parser):
    def __init__(self):
        self._price_selector = ".price-abbr"
        self._search_url = "http://dbs.elmall50.ru/search?l=1&search_field="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.find("span", id="product_price_rub").text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        response = self._send_get_request(url)
        return None if "Извините, но ничего не найдено." in response.text else {search: response.url}

