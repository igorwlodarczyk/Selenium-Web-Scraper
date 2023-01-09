import database.manager as db
import undetected_chromedriver as uc
from zalando.constants import *
from datetime import datetime
from selenium.webdriver.common.by import By
from constants import database_name


class ZalandoScraper(uc.Chrome):
    def __init__(self):
        super(ZalandoScraper, self).__init__()
        self.implicitly_wait(20)
        self.website_name = 'Zalando'
        self.currency = 'PLN'

    def land_page(self, url):
        self.get(url)

    def get_price(self):
        try:
            price = self.find_element(By.XPATH, xpath_price1).text.replace('zł', '').replace(',', '.').replace(' ', '')
        except:
            price = self.find_element(By.XPATH, xpath_price2).text.replace('zł','').replace(',', '.').replace(' ', '')
        price_float = float(price)
        return price_float

    def check_sizes(self):
        size_list = self.find_element(By.XPATH, xpath_size_list)
        if size_list.text != 'One Size':
            size_list.click()
            available_sizes = self.find_elements(By.XPATH, xpath_sizes)
        elif size_list.text == 'One Size':
            available_sizes = ['One Size']
        else:
            available_sizes = []
        return available_sizes

    def save_to_database(self, price_float, available_sizes, item_id):
        time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        for size in available_sizes:
            db.add_data(database_name, item_id, db.get_website_id(database_name, self.website_name), price_float, self.currency, size.text, time)

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



