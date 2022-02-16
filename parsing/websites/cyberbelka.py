import re
from typing import Optional

from requests.cookies import RequestsCookieJar
from selenium.webdriver.common.by import By

from parsing.websites import Parser


class CyberBelkaParser(Parser):
    def __init__(self):
        self._price_selector = ".c-product__price span"
        self._base_url = "https://cyberbelka.ru"
        self._search_url = self._base_url + "/search/?q="

    def parse_model(self, url: str) -> Optional[int]:
        from loader import driver
        driver.get(url)
        try:
            if driver.find_element(By.CSS_SELECTOR, ".i__mini"):
                return
        except:
            pass
        return int(re.findall(r"\d+", driver.find_element(By.CSS_SELECTOR, self._price_selector).text.replace(" ", ""))[0])

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        from loader import driver

        url = self._search_url + search
        models = {}

        driver.get(url)

        models_grid = driver.find_elements(By.CSS_SELECTOR, ".c-product-tile")

        for model in models_grid:
            try:
                model_name = model.find_element(By.CSS_SELECTOR, ".c-product-tile__title").text
                model_url = model.find_element(By.CSS_SELECTOR, ".c-product-tile__link").get_attribute("href")
                models[model_name] = model_url
            except Exception:
                pass

        return models

