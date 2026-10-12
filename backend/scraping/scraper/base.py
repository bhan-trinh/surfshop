from abc import abstractmethod
import re
from backend.scraping.models.product_model import Product
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from backend.scraping import driver

class Scraper:
    def __init__(
            self,
            store,
            product_name_class,
            product_price_class,
            product_amount_class,
            product_card_class,
            search_url_template
        ):
        self.store = store
        self.PRODUCT_CARD_CLASS = product_card_class
        self.PRODUCT_NAME_CLASS = product_name_class
        self.PRODUCT_PRICE_CLASS = product_price_class
        self.PRODUCT_AMOUNT_CLASS = product_amount_class
        self.SEARCH_URL_TEMPLATE = search_url_template


    def scrape_by_product_search(self, search_keyword: str) -> list[Product]:
        driver.get(self.SEARCH_URL_TEMPLATE.format(search_keyword))
        self._setup("by_product_search")

        product_cards = self.scrape_product_cards()
        products = self.parse_product_cards(product_cards)

        return products
    
    
    def scrape_product_cards(self) -> list[WebElement]:
        return driver.find_elements(By.CLASS_NAME, self.PRODUCT_CARD_CLASS)
    
    
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
                name=self._parse_name(card) or "",
                price=self._parse_price(card) or 0,
                amount=self._parse_amount(card) or 0,
                unit=self._parse_unit(card) or "N/A",
            )

            return product

        except Exception as e:
            print("FAILED TO PARSE PRODUCT CARD:", type(e)._name_, e)
            print("CARD HTML:")
            print(card.get_attribute("outerHTML") if card.get_attribute("outerHTML") else "No HTML available")
            return None
    
    def _parse_element(self, card: WebElement, class_name: str) -> str | None:
        try:
            return card.find_element(By.CSS_SELECTOR, f".{class_name}").text
        except Exception as e:
            print(f"FAILED TO PARSE ELEMENT with class '{class_name}':", type(e)._name_, e)
            print("CARD HTML:")
            print(card.get_attribute("outerHTML") if card.get_attribute("outerHTML") else "No HTML available")
            return None
    
    
    def _parse_name(self, card: WebElement) -> str | None:
        return self._parse_element(card, self.PRODUCT_NAME_CLASS)
    
    
    def _parse_price(self, card: WebElement) -> float | None:
        raw_price = self._parse_element(card, self.PRODUCT_PRICE_CLASS)
        return self._extract_price(raw_price)
    
    
    def _parse_amount(self, card: WebElement) -> float | None:
        raw_amount = self._parse_element(card, self.PRODUCT_AMOUNT_CLASS)
        if raw_amount is None:
            return None

        amount, _ = self._extract_amount_and_unit(raw_amount)

        return amount
    
    
    def _parse_unit(self, card: WebElement) -> str | None:
        raw_amount = self._parse_element(card, self.PRODUCT_AMOUNT_CLASS)
        if raw_amount is None:
            return None

        _, unit = self._extract_amount_and_unit(raw_amount)

        return unit
    
    
    def _setup(self, func: str):
        match func:
            case "by_product_search":
                self._setup_by_product_search()
            case "":
                self._setup_default()
            case _:
                raise ValueError(f"Invalid setup function: {func}")
            
    def _setup_by_product_search(self):
        pass
    
    def _setup_default(self):
        pass
    
    def _extract_price(self, raw_str: str | None) -> float | None:
        if raw_str is None:
            return None
        match = re.search(r".*\$(\d\.\d\d)", raw_str)
        return float(match.group(1)) if match else None
    
    
    def _extract_amount_and_unit(self, raw_str: str | None):
        if raw_str is None:
            return None, None
        match = re.search(r"\/(?P<amount>\d*[.]?\d*)\s?(x )?(?P<unit>.*)", raw_str)
        return (
            (float(match.group("amount")), match.group("unit")) if match else (None, None)
        )

