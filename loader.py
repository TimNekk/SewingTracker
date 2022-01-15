import sys
import logging
from logging import StreamHandler, Formatter

from parsing.parsers_handler import ParsersHandler
from utils.db_api.sqlite import Database

db = Database()
ph = ParsersHandler()
logging.basicConfig(level=logging.INFO, format="[%(asctime)s: %(levelname)s] %(message)s")

# handler = StreamHandler(stream=sys.stdout)
# handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
# logger.addHandler(handler)
