from typing import override

from backend.scraping.scraper.base import Scraper
import time
from backend.scraping import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TraderJoesScraper(Scraper):
    PRODUCT_CARD_CLASS = "SearchResultCard_searchResultCard__3V-_h"
    PRODUCT_NAME_CLASS = "SearchResultCard_searchResultCard__titleLink__2nz6x"
    PRODUCT_PRICE_CLASS = "ProductPrice_productPrice__price__3-50j"
    PRODUCT_AMOUNT_CLASS = "ProductPrice_productPrice__unit__2jvkA"
    SEARCH_URL_TEMPLATE = "https://www.traderjoes.com/home/search?q={}"
    
    def __init__(self):
        super().__init__(
            store="Trader Joe's",
            product_card_class=self.PRODUCT_CARD_CLASS,
            product_name_class=self.PRODUCT_NAME_CLASS,
            product_price_class=self.PRODUCT_PRICE_CLASS,
            product_amount_class=self.PRODUCT_AMOUNT_CLASS,
            search_url_template=self.SEARCH_URL_TEMPLATE
        )
    
    @override
    def _setup_by_product_search(self):
        SLEEP_SEC = 2
        
        time.sleep(SLEEP_SEC)
        COOKIE_BUTTON = driver.find_element(By.CLASS_NAME, "Button_button_variant_secondary__RwIii")
        COOKIE_BUTTON.click()
        
        time.sleep(SLEEP_SEC)
        LOAD_MORE_BUTTON = driver.find_element(By.CLASS_NAME, "SearchResults_searchResults__sectionButton__2pbDw")
        ActionChains(driver).scroll_to_element(LOAD_MORE_BUTTON).perform()
        LOAD_MORE_BUTTON.click()

        time.sleep(SLEEP_SEC)
        
