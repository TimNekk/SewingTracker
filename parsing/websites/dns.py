import re

from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

from parsing.websites import Parser
from parsing.websites.parser import ParseException


class DNSParser(Parser):
    def __init__(self):
        self._price_selector = ".product-buy__price"
        self._search_url = "https://www.dns-shop.ru/search/?q="

    def parse_model(self, url: str) -> int:
        from loader import driver
        driver.get(url)

        try:
            price = int(re.findall(r"\d+", driver.find_element(By.CSS_SELECTOR, self._price_selector).text.replace(" ", ""))[0])
            return price
        except Exception:
            raise ParseException("Товара нет в наличии")

    def parse_search(self, search: str) -> dict[str, str]:
        from loader import driver

        url = self._search_url + search
        models = {}

        driver.get(url)
        if "product" in driver.current_url:
            return {search: driver.current_url}

        models_grid = driver.find_elements(By.CSS_SELECTOR, ".catalog-product__name")

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text.split("[")[0]).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = model.get_attribute("href")
                    models[model_name] = model_url
            except Exception:
                pass

        return models

