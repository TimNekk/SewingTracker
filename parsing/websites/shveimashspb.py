import re

from parsing.websites import Parser


class ShveiMashSpbParser(Parser):
    def __init__(self):
        self._price_selector = "#catalog_element .wrapper_price .price"

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price