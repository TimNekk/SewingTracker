import re

from parsing.websites import Parser


class SewingKingParser(Parser):
    def __init__(self):
        self._price_selector = ".product-info .form-group .list-unstyled .update_price, .product-info .form-group .list-unstyled .update_special"

    def parse(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price
