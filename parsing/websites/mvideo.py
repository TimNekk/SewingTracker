import logging
import re
from pprint import pprint

from requests.cookies import RequestsCookieJar

from parsing.websites import Parser


class MvideoParser(Parser):
    def __init__(self):
        self._base_url = "https://www.mvideo.ru/"
        self._search_url = self._base_url + "bff/products/search?query="
        self._list_url = self._base_url + "bff/product-details/list"
        self._price_url = self._base_url + "bff/products/prices"
        self._status_url = self._base_url + "bff/product-details/status"

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

    def parse_model(self, url: str) -> int:
        product_id = self._get_product_id(url)
        params = self._get_parse_params(product_id)
        cookies = self._get_cookies()

        response = self._send_get_request(self._status_url, params=params, cookies=cookies).json()
        if response.get("body").get("status").get("showPrice"):
            response = self._send_get_request(self._price_url, params=params, cookies=cookies).json()
            return response.get("body").get("materialPrices")[0].get("price").get("salePrice")

    # def parse_search(self, search: str) -> dict[str, str]:
    #     # ПРАРСИТ ТОЛЬКО ПЕРВУЮ СТРАНИЦУ!!!
    #
    #     url = self._search_url + search.replace(" ", "+")
    #     models = {}
    #     page = 1
    #
    #     while True:
    #         cookies = self._get_cookies()
    #         ids = self._send_get_request(self._search_url + search, cookies=cookies).json().get("body").get("products")
    #
    #         data = {
    #             "productIds": [
    #                 "20032054"
    #             ],
    #             "mediaTypes": [
    #                 "images"
    #             ],
    #             "category": True,
    #             "status": True,
    #             "brand": True,
    #             "propertyTypes": [
    #                 "KEY"
    #             ],
    #             "propertiesConfig": {
    #                 "propertiesPortionSize": 5
    #             },
    #             "multioffer": False
    #         }
    #         print(self._send_post_request(self._list_url, data=data, cookies=cookies))
    #         return
    #         # soup = self._get_soup(url + f"&page={page}")
    #
    #         models_grid = soup.select(".product-cards-row[_ngcontent-serverapp-c194]")
    #         print(models_grid)
    #
    #         for models3 in models_grid:
    #             try:
    #                 model_names_a = models3.select(".product-title__text[_ngcontent-serverapp-c202]")
    #                 for model_name_a in model_names_a:
    #                     model_name = model_name_a.text
    #                     model_url = self._base_url + model_name_a['href']
    #                     models[model_name] = model_url
    #             except Exception as e:
    #                 logging.error(e)
    #
    #         break
    #
    #     return models
