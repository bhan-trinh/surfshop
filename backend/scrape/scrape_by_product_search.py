
import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from backend.services.setup_service import (
    close_cookie_panel,
    close_address_panel,
    scroll_to_load,
)
from selenium.webdriver.remote.webelement import WebElement

"""
NOTE:
- Make a game with an ecosystem (e.g. Rain World)
- Make a game with an inventory and item system (e.g. Stardew Valley)
"""
import sys

from backend import driver
from backend.models.product_model import Product

def scrape_by_product_search(
    search_keyword: str,
    store: str
) -> list[Product] | None:
    match store.lower():
        case "aldi":
            return aldi_scrape_by_product_search(search_keyword)
    
    return None
            
            
def aldi_scrape_by_product_search(search_keyword: str) -> list[Product]:
    driver.get("https://www.aldi.us/store/aldi/s?k={}".format(search_keyword))
    
    SLEEP_SEC = 2
    time.sleep(SLEEP_SEC)
    close_cookie_panel()
    
    time.sleep(SLEEP_SEC)
    close_address_panel()
    
    time.sleep(SLEEP_SEC)
    scroll_to_load()
    
    PRODUCT_CARD_CLASS = "e-1aytrge"

    product_cards = driver.find_elements(By.CLASS_NAME, PRODUCT_CARD_CLASS)
    print("CARDS:", len(product_cards))
    
    products: list[Product] = []
    
    for card in product_cards:
        product = aldi_scrape_by_product_card(card)
        if product:
            products.append(product)
    
    print("PRODUCTS:", len(products))
    
    return products
        
        
def aldi_scrape_by_product_card(card: WebElement) -> Product | None:
    PRODUCT_PRICE_CLASS = "e-1632met"
    PRODUCT_PRICE_CLASS_2 = "e-1n0a46q"
    
    PRODUCT_NAME_CLASS = "e-1gh06cz"
    PRODUCT_AMOUNT_CLASS = "e-1r6exdz"
    
    try:
        raw_product_current_price = card.find_element(
            By.CSS_SELECTOR, f".{PRODUCT_PRICE_CLASS}"
        ).text
    except Exception as e:
        try:
            raw_product_current_price = card.find_element(
                By.CSS_SELECTOR, f".{PRODUCT_PRICE_CLASS_2}"
            ).text
            print("ERROR: Price class 1 doesn't work. Trying Price class 2.")
            print("CARD HTML:")
            print(card.get_attribute("outerHTML")[:3000])
        
        except Exception as e:
            print("FAILED:", type(e).__name__, e)
            print("CARD HTML:")
            print(card.get_attribute("outerHTML")[:3000])
            return None

    raw_product_name = card.find_element(
        By.CSS_SELECTOR, f".{PRODUCT_NAME_CLASS}"
    ).text

    raw_product_amount = card.find_element(
        By.CSS_SELECTOR, f".{PRODUCT_AMOUNT_CLASS}"
    ).text

    product_current_price = extract_price(raw_product_current_price)
    product_amount, product_unit = extract_amount_and_unit(raw_product_amount)

    product = Product(
        name=raw_product_name,
        price=product_current_price or 0,
        amount=product_amount or 0,
        unit=product_unit or "N/A",
    )
    
    return product
    

        
def extract_price(raw_str: str):
    match = re.search(r"Current price: \$(\d\.\d\d)", raw_str)
    return float(match.group(1)) if match else None


def extract_amount_and_unit(raw_str: str):
    match = re.search(r"(?P<amount>\d*.?\d*)\s(x )?(?P<unit>.*)", raw_str)
    return (float(match.group("amount")), match.group("unit")) if match else (None, None)
            
            
            

