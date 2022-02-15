from parsing.websites.ozon import OzonParser


class ShveyberiOzonParser(OzonParser):
    def __init__(self):
        super().__init__()
        self._search_url = self._base_url + "/seller/shveyberi-74775/products/?from_global=true&text="
