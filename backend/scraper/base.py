from abc import abstractmethod
import re
from backend.models.product_model import Product
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class Scraper:
    def __init__(
            self,
            store,
            product_name_class,
            product_price_class,
            product_amount_class
        ):
        self.store = store
        self.PRODUCT_NAME_CLASS = product_name_class
        self.PRODUCT_PRICE_CLASS = product_price_class
        self.PRODUCT_AMOUNT_CLASS = product_amount_class


    def scrape_by_product_search(self, search_keyword: str) -> list[Product]:
        product_cards = self.scrape_product_cards(search_keyword)
        products = self.parse_product_cards(product_cards)

        return products
    
    
    @abstractmethod
    def scrape_product_cards(self, search_keyword: str) -> list[WebElement]:
        pass
    
    
    def parse_product_cards(self, product_cards) -> list[Product]:
        products: list[Product] = []

        for card in product_cards:
            product = self.parse_one_product_card(card)
            if product:
                products.append(product)
        return products
    
    
    def parse_one_product_card(self, card: WebElement) -> Product | None:
        try:
            product = Product(
                name=self.__parse_name(card) or "",
                price=self.__parse_price(card) or 0,
                amount=self.__parse_amount(card) or 0,
                unit=self.__parse_unit(card) or "N/A",
            )

            return product

        except Exception as e:
            print("FAILED TO PARSE PRODUCT CARD:", type(e).__name__, e)
            print("CARD HTML:")
            print(card.get_attribute("outerHTML") if card.get_attribute("outerHTML") else "No HTML available")
            return None
    
    
    def __parse_element(self, card: WebElement, class_name: str) -> str | None:
        try:
            return card.find_element(By.CSS_SELECTOR, f".{class_name}").text
        except Exception as e:
            print(f"FAILED TO PARSE ELEMENT with class '{class_name}':", type(e).__name__, e)
            print("CARD HTML:")
            print(card.get_attribute("outerHTML") if card.get_attribute("outerHTML") else "No HTML available")
            return None
    
    
    def __parse_name(self, card: WebElement) -> str | None:
        return self.__parse_element(card, self.PRODUCT_NAME_CLASS)
    
    
    def __parse_price(self, card: WebElement) -> float | None:
        raw_price = self.__parse_element(card, self.PRODUCT_PRICE_CLASS)
        return self.__extract_price(raw_price)
    
    
    def __parse_amount(self, card: WebElement) -> float | None:
        raw_amount = self.__parse_element(card, self.PRODUCT_AMOUNT_CLASS)
        if raw_amount is None:
            return None

        amount, _ = self.__extract_amount_and_unit(raw_amount)

        return amount
    
    
    def __parse_unit(self, card: WebElement) -> str | None:
        raw_amount = self.__parse_element(card, self.PRODUCT_AMOUNT_CLASS)
        if raw_amount is None:
            return None

        _, unit = self.__extract_amount_and_unit(raw_amount)

        return unit
    
    
    def __extract_price(self, raw_str: str | None) -> float | None:
        if raw_str is None:
            return None
        match = re.search(r".*\$(\d\.\d\d)", raw_str)
        return float(match.group(1)) if match else None
    
    
    def __extract_amount_and_unit(self, raw_str: str | None):
        if raw_str is None:
            return None, None
        match = re.search(r"\/(?P<amount>\d*[.]?\d*)\s?(x )?(?P<unit>.*)", raw_str)
        return (
            (float(match.group("amount")), match.group("unit")) if match else (None, None)
        )

