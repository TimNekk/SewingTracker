from parsing.websites.ozon import OzonParser


class SewingKingdomOzonParser(OzonParser):
    def __init__(self):
        super().__init__()
        self._search_url = self._base_url + "/seller/ooo-shveynoe-korolevstvo-147310/products/?from_global=true&text="
