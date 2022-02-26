from parsing.websites.ozon import OzonParser


class SewCityOzonParser(OzonParser):
    def __init__(self):
        super().__init__()
        self._search_url = self._base_url + "/seller/sewcity-20801/products/?from_global=true&text="
        self._name_xpath = '//*[@id="layoutPage"]/div[1]/div[7]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/a'
