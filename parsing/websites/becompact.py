import re
from typing import Optional
from time import sleep

from selenium.webdriver.common.by import By

from parsing.websites import Parser


class BeCompactParser(Parser):
    def __init__(self):
        self._price_selector = ".product-price__new"
        self._base_url = "https://becompact.ru"
        self._search_url = self._base_url + "/search?q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        from loader import driver

        url = self._search_url + search
        models = {}

        driver.get(url)

        while True:
            models_grid = driver.find_elements(By.CSS_SELECTOR, ".block-product-card__data .block-product-card__name")
            try:
                if driver.find_element(By.CSS_SELECTOR, ".block-column__title"):
                    return
            except:
                pass
            sleep(0.5)
            if models_grid:
                break

        for model in models_grid:
            try:
                model_name = model.text
                model_url = model.get_attribute("href")
                models[model_name] = model_url
            except Exception:
                pass

        return models

