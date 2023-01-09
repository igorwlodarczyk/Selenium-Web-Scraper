from zalando.zalando import ZalandoScraper
from end_clothing.end_clothing import EndClothingScraper


driver = ZalandoScraper()
driver.scrap_data()
driver2 = EndClothingScraper()
driver2.scrap_data()
