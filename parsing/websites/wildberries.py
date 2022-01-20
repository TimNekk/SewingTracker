import re

from parsing.websites import Parser


class WildberriesParser(Parser):
    def __init__(self):
        self._price_selector = ".same-part-kt .price-block__final-price"

    def parse(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price