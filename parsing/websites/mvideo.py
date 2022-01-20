import re
from pprint import pprint

from requests.cookies import RequestsCookieJar

from parsing.websites import Parser


class MvideoParser(Parser):
    def __init__(self):
        self._base_url = "https://www.mvideo.ru/"
        self._price_url = self._base_url + "bff/products/prices"

    @staticmethod
    def _get_product_id(url: str) -> int:
        return int(re.findall(r"\d+", url)[-1])

    @staticmethod
    def _get_parse_params(product_id: int) -> dict:
        return {
            "productIds": product_id,
            "isPromoApplied": True,
            "addBonusRubles": True,
            "isPricingEngineFinalPrice": True
        }

    def _get_cookies(self) -> RequestsCookieJar:
        return self._send_get_request(self._base_url).cookies

    def parse(self, url: str) -> int:
        product_id = self._get_product_id(url)
        params = self._get_parse_params(product_id)
        cookies = self._get_cookies()

        response = self._send_get_request(self._price_url, params=params, cookies=cookies).json()
        return response.get("body").get("materialPrices")[0].get("price").get("salePrice")

