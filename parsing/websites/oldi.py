import re
from time import sleep
from typing import Optional

from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

from parsing.websites import Parser
from parsing.websites.parser import ParseException


class OldiParser(Parser):
    def __init__(self):
        self._price_selector = ".cte_w_price"
        self._base_url = "https://www.oldi.ru"
        self._search_url = self._base_url + "/?digiSearch=true&params=%7Csort%3DDEFAULT&term="

    def parse_model(self, url: str) -> int:
        from loader import driver
        driver.get(url)

        try:
            price = int(re.findall(r"\d+", driver.find_element(By.CSS_SELECTOR, self._price_selector).text.replace(" ", ""))[0])
            return price
        except Exception:
            raise ParseException("Товара нет в наличии")

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        from loader import driver

        url = self._search_url + search
        models = {}

        driver.get(url)

        while True:
            models_grid = driver.find_elements(By.CSS_SELECTOR, "#digi-shield .digi-product__label")
            sleep(0.5)
            if models_grid:
                break

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text.split("[")[0]).strip()

                if fuzz.ratio(model_name, search) >= 95:
                    model_url = model.get_attribute("href")
                    models[model_name] = model_url
            except Exception:
                pass

        return models

