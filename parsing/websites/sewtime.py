import re
from typing import Optional

from selenium.webdriver.common.by import By

from parsing.websites import Parser


class SewTimeParser(Parser):
    def __init__(self):
        self._price_selector = ".product-item-detail-price-current"
        self._base_url = "https://sewtime.ru"
        self._search_url = self._base_url + "/search/?how=r&q=merrylock"

    def parse_model(self, url: str) -> Optional[int]:
        soup = self._get_soup(url)
        try:
            price = int("".join(re.findall(r"\d+", soup.select_one(self._price_selector).text)))
        except ValueError:
            return
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        from loader import driver

        url = self._search_url + search
        models = {}

        driver.get(url)
        models_grid = driver.find_element(By.CLASS_NAME, "search-page")
        print(models_grid)
        models_grid = models_grid.find_element(By.TAG_NAME, "a")
        print(models_grid)
        return

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text.split("[")[0]).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = model.get_attribute("href")
                    models[model_name] = model_url
            except Exception:
                pass

        return models

