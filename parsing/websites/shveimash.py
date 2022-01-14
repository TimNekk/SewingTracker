from parsing.websites import Parser


class ShveiMashParser(Parser):
    def __init__(self):
        self._price_selector = ".t-store__card__price-currency, .t-store__card__price-value, .t-store__prod-popup__price-currency, .t-store__prod-popup__price-value, .t-store__prod__price-portion"

    def parse(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(float(soup.select_one(self._price_selector).text.replace(",", ".")))
        return price