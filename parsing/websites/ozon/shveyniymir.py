from parsing.websites.ozon import OzonParser


class ShveyniyMirOzonParser(OzonParser):
    def __init__(self):
        super().__init__()
        self._search_url = self._base_url + "/seller/kompaniya-shveynyy-mir-67163/products/?from_global=true&text="
