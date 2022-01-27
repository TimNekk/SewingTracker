from parsing.websites import Parser


class ShveiMashParser(Parser):
    def __init__(self):
        self._price_selector = ".t-store__card__price-currency, .t-store__card__price-value, .t-store__prod-popup__price-currency, .t-store__prod-popup__price-value, .t-store__prod__price-portion"
        self._search_url = "https://search.tildacdn.com/search/?p=2840209&q="

    def parse_model(self, url: str) -> int:
        soup = self._get_soup(url)
        price = int(float(soup.select_one(self._price_selector).text.replace(",", ".")))
        return price

    def parse_search(self, search: str) -> dict[str, str]:
        url = self._search_url + search
        models = {}
        page = 1

        while True:
            response = self._send_get_request(url + f"&page={page}").json()
            models_list = response.get("pages")

            if not models_list:
                break

            for model in models_list:
                if model.get("product"):
                    try:
                        model_name = model.get("title")
                        model_url = model.get("pageurl")
                        models[model_name] = model_url
                    except Exception:
                        pass

            page += 1

        return models