import time
from typing import override

from backend.scraper.base import Scraper
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from backend.services.setup_service import close_cookie_panel, scroll_to_load

from backend import driver
from selenium.webdriver.common.action_chains import ActionChains

class AldiScraper(Scraper):
    PRODUCT_CARD_CLASS = "e-1aytrge"
    PRODUCT_NAME_CLASS = "e-1gh06cz"
    PRODUCT_PRICE_CLASS = "e-1632met"
    PRODUCT_PRICE_CLASS_2 = "e-1n0a46q"
    PRODUCT_AMOUNT_CLASS = "e-1r6exdz"
    SEARCH_URL_TEMPLATE = "https://www.aldi.us/en/search/?q={}"
    
    def __init__(self):
        super().__init__(
            store="Aldi",
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
        self.__close_cookie_panel()
    
        time.sleep(SLEEP_SEC)
        self.__close_address_panel()
    
        time.sleep(SLEEP_SEC)
        self.__scroll_to_load()
        
    @override
    def _parse_price(self, card: WebElement) -> float | None:
        try:
            raw_price = card.find_element(
                By.CSS_SELECTOR, f".{self.PRODUCT_PRICE_CLASS}"
            ).text

        except Exception:
            try:
                raw_price = card.find_element(
                    By.CSS_SELECTOR, f".{self.PRODUCT_PRICE_CLASS_2}"
                ).text

                print("ERROR: Price class 1 doesn't work. Trying Price class 2.")
                print("CARD HTML:")
                print(card.get_attribute("outerHTML")[:3000])

            except Exception as e:
                print("FAILED:", type(e).__name__, e)
                print("CARD HTML:")
                print(card.get_attribute("outerHTML")[:3000])
                return None

        return self._extract_price(raw_price)
    
    
    def __scroll_to_load(self):
        try:
            LOAD_MORE_BUTTON = driver.find_element(By.CLASS_NAME, "e-1o3e8yi")
            ActionChains(driver).scroll_to_element(LOAD_MORE_BUTTON).perform()
        except Exception as e:
            print("ERROR: Can't find Load More button.")
            print(e)


    def __close_address_panel(self):
        """Closes panel confirming delivery address."""
        try:
            CONFIRM_ADDR_CLASS = "e-182rjqr"
            driver.find_element(By.CLASS_NAME, CONFIRM_ADDR_CLASS).click()
        except Exception as e:
            print("ERROR: Can't find Delivery Address Confirm button.")
            print(e)


    def __close_cookie_panel(self):
        try:
            COOKIE_REJECT_ID = "onetrust-reject-all-handler"
            driver.find_element(By.ID, COOKIE_REJECT_ID).click()
        except Exception as e:
            print("ERROR: Can't find Cookie Reject button.")
            print(e)