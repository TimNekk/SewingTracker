from parsing.websites import *


class ParsersHandler:
    def __init__(self):
        self.parsers = {
            "mvideo": MvideoParser,
            "shvei-mash": ShveiMashParser
        }

    def parse(self, market_name: str, model_url: str) -> int:
        parser = self._get_parser(market_name)
        parse_result = parser.parse(model_url)
        return parse_result

    def _get_parser(self, market_name: str) -> Parser:
        parser = self.parsers.get(market_name)
        if parser is None:
            raise ValueError(f"No parser found for market \"{market_name}\"")
        return parser()
