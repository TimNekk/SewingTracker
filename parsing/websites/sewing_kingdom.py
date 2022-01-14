from requests import Session
from bs4 import BeautifulSoup as BS
from re import findall

from data.config import default_headers
from classes.product import Product


url = "https://sewing-kingdom.ru/index.php?route=product/search&search=necchi"


def get_products_from_sewing_kingdom():
    with Session() as sess:
        sess.headers = default_headers

        resp = sess.get(url)

        if resp.status_code != 200:
            print(resp)
            return

        soup = BS(resp.content, "html.parser")

        products_grid = soup.find("div", class_="product-list")
        products = []

        for product_item in products_grid:
            try:
                name = product_item.find("div", class_="name").find("a").text
                price = int(findall(r"\d+", product_item.find("div", class_="price").text)[0])
                article = int(findall(r"\d+", product_item.find("div", class_="extra").text)[0])
                product = Product(name, article, price)
                products.append(product)
            except:
                continue

        return products
