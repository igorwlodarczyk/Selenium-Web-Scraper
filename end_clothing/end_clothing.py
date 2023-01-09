import database.manager as db
import undetected_chromedriver as uc
from end_clothing.constants import *
from selenium.webdriver.common.by import By
from constants import database_name
from datetime import datetime


class EndClothingScraper(uc.Chrome):
    def __init__(self):
        super(EndClothingScraper, self).__init__()
        self.implicitly_wait(20)
        self.website_name = 'End Clothing'
        self.currency = 'EUR'

    def land_page(self, url):
        self.get(url)

    def get_price(self):
        price = float(self.find_element(By.ID, price_id).text.replace("EUR€", ""))
        return price

    def check_sizes(self):
        available_sizes = self.find_elements(By.CSS_SELECTOR, css_selector_size)
        return available_sizes

    def save_to_database(self, price_float, available_sizes, item_id):
        time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        for size in available_sizes:
            db.add_data(database_name, item_id, db.get_website_id(database_name, self.website_name), price_float,
                        self.currency, size.text, time)

    def get_urls_from_database(self):
        website_id = db.get_website_id(database_name, self.website_name)
        urls_item_id = db.get_urls_item_id(database_name, website_id)
        return urls_item_id

    def scrap_data(self):
        urls_item_id = self.get_urls_from_database()
        for url in urls_item_id:
            self.land_page(url)
            price_float = self.get_price()
            available_sizes = self.check_sizes()
            self.save_to_database(price_float, available_sizes, urls_item_id[url])
