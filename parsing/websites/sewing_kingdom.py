import re

from parsing.websites import Parser


class SewingKingdomParser(Parser):
    def __init__(self):
        self._price_selector = ".pmip_buy_price"

    def parse(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text)[0])
        return price
