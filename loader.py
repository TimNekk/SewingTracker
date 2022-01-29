import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parsing.parsers_handler import ParsersHandler
from utils.db_api.sqlite import Database

db = Database()
ph = ParsersHandler()
logging.basicConfig(level=logging.INFO, format="[%(asctime)s: %(levelname)s] %(message)s")

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)