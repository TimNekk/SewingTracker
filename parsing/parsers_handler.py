import logging

from parsing.websites import *


class ParsersHandler:
    def __init__(self):
        self.parsers = {
            "mvideo": MvideoParser,
            "shvei-mash": ShveiMashParser,
            "shveimash-spb": ShveiMashSpbParser,
            "sewing-kingdom": SewingKingdomParser,
            "sewingking": SewingKingParser,
            "textiletorg": TextiletorgParser,
            "holodilnik": HolodilnikParser,
            "citilink": CitilinkParser,
            "sewingstore": SewingStoreParser,
            "dns": DNSParser,
            "techport": TechPortParser,
            "kcentr": KcentrParser,
            "kulturabt": KulturabtParser,
            "elecity": ElecityParser,
            "sewingadvisor": SewingAdvisorParser,
            "ozon-sewingadvisor": SewingAdvisorOzonParser,
            "ozon-shveyniymir": ShveyniyMirOzonParser,
            "ozon-sewing-kingdom": SewingKingdomOzonParser,
            "ozon-sewcity": SewCityOzonParser,
            "ozon-1001": Ozon1001Parser,
            "ozon-sofia": SofiaOzonParser,
            "ozon-shveyberi": ShveyberiOzonParser,
            "just": JustParser,
            "becompact": BeCompactParser,
            "oldi": OldiParser,
            "elmall": ElMallParser,
            "2bit": Bit2Parser,
            "skyey": SkyeyParser,
            "cyberbelka": CyberBelkaParser,
            "123": S123Parser,
            "veritaz": VeritazParser,
            "weektrade": WeekTradeParser,
            "damadoma": DamaDomaParser,
        }

    def parse_model(self, market_name: str, model_url: str) -> int:
        parser = self._get_parser(market_name)
        logging.info(f"Parsing {model_url} in {market_name}...")
        parse_result = parser.parse_model(model_url)
        logging.info("Done!")
        return parse_result

    def parse_search(self, market_name: str, search: str) -> dict[str, str]:
        parser = self._get_parser(market_name)
        logging.info(f"Searching {market_name} for \"{search}\" url...")
        parse_result = parser.parse_search(search)
        logging.info("Done!")
        return parse_result

    def _get_parser(self, market_name: str) -> Parser:
        parser = self.parsers.get(market_name)
        if parser is None:
            raise ValueError(f"No parser found for market \"{market_name}\"")
        return parser()
