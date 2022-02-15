from parsing.websites.ozon import OzonParser


class SewCityOzonParser(OzonParser):
    def __init__(self):
        super().__init__()
        self._search_url = self._base_url + "/seller/sewcity-20801/products/?from_global=true&text="
