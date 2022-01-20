import logging

from parsing.websites import *


class ParsersHandler:
    def __init__(self):
        self.parsers = {
            "mvideo": MvideoParser,
            "shvei-mash": ShveiMashParser,
            "sewing-kingdom": SewingKingdomParser,
            "sewingking": SewingKingParser,
            "textiletorg": TextiletorgParser,
            "ozon-sewing-store": OzonParser,
            "ozon-gg": OzonParser,
            "wildberries": WildberriesParser,
        }

    def parse(self, market_name: str, model_url: str) -> int:
        parser = self._get_parser(market_name)
        logging.info(f"Parsing {model_url} in {market_name}...")
        parse_result = parser.parse(model_url)
        logging.info("Done!")
        return parse_result

    def _get_parser(self, market_name: str) -> Parser:
        parser = self.parsers.get(market_name)
        if parser is None:
            raise ValueError(f"No parser found for market \"{market_name}\"")
        return parser()
