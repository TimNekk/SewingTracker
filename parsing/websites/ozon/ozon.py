import re
from typing import Optional

from fuzzywuzzy import fuzz
from lxml import etree

from parsing.websites import Parser


class OzonParser(Parser):
    def __init__(self):
        self._price_xpath = '//*[@id="layoutPage"]/div[1]/div[4]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/span[1]/span'
        self._name_xpath = '//*[@id="layoutPage"]/div[1]/div[5]/div/div[2]/div[2]/div/div/div/div[1]/div[1]/a'
        self._base_url = "https://ozon.com"
        self._search_url = self._base_url + "/search/?from_global=true&text="

    def parse_model(self, url: str) -> int:
        response = self._send_get_request(url)
        tree = etree.HTML(response.content)
        price = int("".join(re.findall(r"\d+", tree.xpath(self._price_xpath)[0].text)))
        return price

    def parse_search(self, search: str) -> Optional[dict[str, str]]:
        url = self._search_url + search
        models = {}

        response = self._send_get_request(url)
        tree = etree.HTML(response.content)
        model = tree.xpath(self._name_xpath)[0]

        model_name = re.sub(r"[а-яА-Я]+", "", model.xpath('span/span')[0].text).strip()

        if fuzz.ratio(model_name.lower(), search.lower()) >= 93:
            model_url = self._base_url + model.attrib['href']
            models[model_name] = model_url

        return models
