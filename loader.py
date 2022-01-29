import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from parsing.parsers_handler import ParsersHandler
from utils.db_api.sqlite import Database

db = Database()
ph = ParsersHandler()
logging.basicConfig(level=logging.INFO, format="[%(asctime)s: %(levelname)s] %(message)s")

chrome_options = Options()
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)