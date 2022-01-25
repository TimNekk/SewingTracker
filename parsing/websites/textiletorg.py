import re

from parsing.websites import Parser


class TextiletorgParser(Parser):
    def __init__(self):
        self._price_selector = "#item .right_block_cart .price-price"

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(soup.select_one(self._price_selector).text.replace(" ", ""))
        return price
