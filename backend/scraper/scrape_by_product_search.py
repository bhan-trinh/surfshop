import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from backend.scrape.tjoe import tjoe_parse_amount, tjoe_parse_name, tjoe_parse_price, tjoe_parse_unit
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
from backend import driver
from backend.models.product_model import Product


def scrape_by_product_search(search_keyword: str, store: str) -> list[Product] | None:
    match store.lower():
        case "aldi":
            return aldi_scrape_by_product_search(search_keyword)
        case "tjoe":
            return tjoe_scrape_by_product_search(search_keyword)

    return None


def aldi_scrape_by_product_search(search_keyword: str) -> list[Product]:
    product_cards = aldi_scrape_product_cards(search_keyword)
    products = aldi_parse_product_cards(product_cards)

    return products


def tjoe_scrape_by_product_search(search_keyword: str) -> list[Product]:
    product_cards = tjoe_scrape_product_cards(search_keyword)
    products = tjoe_parse_product_cards(product_cards)

    return products


def tjoe_scrape_product_cards(search_keyword):
    driver.get("https://www.traderjoes.com/home/search?q={}".format(search_keyword))

    SLEEP_SEC = 2
    
    time.sleep(SLEEP_SEC)
    COOKIE_BUTTON = driver.find_element(By.CLASS_NAME, "Button_button_variant_secondary__RwIii")
    COOKIE_BUTTON.click()
    
    time.sleep(SLEEP_SEC)
    LOAD_MORE_BUTTON = driver.find_element(By.CLASS_NAME, "SearchResults_searchResults__sectionButton__2pbDw")
    ActionChains(driver).scroll_to_element(LOAD_MORE_BUTTON).perform()
    LOAD_MORE_BUTTON.click()

    time.sleep(SLEEP_SEC)
    
    PRODUCT_CARD_CLASS = "SearchResultCard_searchResultCard__3V-_h"

    product_cards = driver.find_elements(By.CLASS_NAME, PRODUCT_CARD_CLASS)
    
    return product_cards


def tjoe_parse_product_cards(product_cards):
    products: list[Product] = []

    for card in product_cards:
        product = tjoe_parse_product_card(card)
        if product:
            products.append(product)
    return products



def tjoe_parse_product_card(card: WebElement) -> Product | None:
    try:
        product = Product(
            name=tjoe_parse_name(card),
            price=tjoe_parse_price(card) or 0,
            amount=tjoe_parse_amount(card) or 0,
            unit=tjoe_parse_unit(card) or "N/A",
        )

        return product

    except Exception as e:
        print("FAILED TO PARSE PRODUCT CARD:", type(e).__name__, e)
        print("CARD HTML:")
        print(card.get_attribute("outerHTML")[:3000])
        return None


def aldi_parse_product_cards(product_cards):
    products: list[Product] = []

    for card in product_cards:
        product = aldi_parse_product_card(card)
        if product:
            products.append(product)
    return products


def aldi_scrape_product_cards(search_keyword):
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
    return product_cards


def aldi_parse_name(card: WebElement) -> str:
    PRODUCT_NAME_CLASS = "e-1gh06cz"

    return card.find_element(
        By.CSS_SELECTOR, f".{PRODUCT_NAME_CLASS}"
    ).text


def aldi_parse_price(card: WebElement) -> float | None:
    PRODUCT_PRICE_CLASS = "e-1632met"
    PRODUCT_PRICE_CLASS_2 = "e-1n0a46q"

    try:
        raw_price = card.find_element(
            By.CSS_SELECTOR, f".{PRODUCT_PRICE_CLASS}"
        ).text

    except Exception:
        try:
            raw_price = card.find_element(
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

    return extract_price(raw_price)


def aldi_parse_amount(card: WebElement) -> float | None:
    PRODUCT_AMOUNT_CLASS = "e-1r6exdz"

    raw_amount = card.find_element(
        By.CSS_SELECTOR, f".{PRODUCT_AMOUNT_CLASS}"
    ).text

    amount, _ = extract_amount_and_unit(raw_amount)

    return amount


def aldi_parse_unit(card: WebElement) -> str | None:
    PRODUCT_AMOUNT_CLASS = "e-1r6exdz"

    raw_amount = card.find_element(
        By.CSS_SELECTOR, f".{PRODUCT_AMOUNT_CLASS}"
    ).text

    _, unit = extract_amount_and_unit(raw_amount)

    return unit


def aldi_parse_product_card(card: WebElement) -> Product | None:
    try:
        product = Product(
            name=aldi_parse_name(card),
            price=aldi_parse_price(card) or 0,
            amount=aldi_parse_amount(card) or 0,
            unit=aldi_parse_unit(card) or "N/A",
        )

        return product

    except Exception as e:
        print("FAILED TO PARSE PRODUCT CARD:", type(e).__name__, e)
        print("CARD HTML:")
        print(card.get_attribute("outerHTML")[:3000])
        return None


def extract_price(raw_str: str):
    match = re.search(r"Current price: \$(\d\.\d\d)", raw_str)
    return float(match.group(1)) if match else None


def extract_amount_and_unit(raw_str: str):
    match = re.search(r"(?P<amount>\d*[.]?\d*)\s?(x )?(?P<unit>.*)", raw_str)
    return (
        (float(match.group("amount")), match.group("unit")) if match else (None, None)
    )
