import re

from parsing.websites import Parser


class OzonParser(Parser):
    def __init__(self):
        self._price_selector = ".n6j .nj7"

    def parse(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", "").replace(" ", ""))[0])
        return price