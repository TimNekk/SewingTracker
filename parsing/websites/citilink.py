import re

from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

from parsing.websites import Parser


class CitilinkParser(Parser):
    def __init__(self):
        self._price_selector = ".ProductHeader__price-default"
        self._base_url = "https://www.citilink.ru"
        self._search_url = self._base_url + "/search/?text="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(re.findall(r"\d+", soup.select_one(self._price_selector).text.replace(" ", ""))[0])
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        from loader import driver

        url = self._search_url + search
        models = {}

        driver.get(url)
        models_grid = driver.find_elements(By.CSS_SELECTOR, ".ProductCardVertical__name")

        for model in models_grid:
            try:
                model_name = re.sub(r"[а-яА-Я]+", "", model.text).strip()

                if fuzz.ratio(model_name, search) >= 96:
                    model_url = model.get_attribute("href")
                    models[model_name] = model_url
            except Exception:
                pass

        return models

