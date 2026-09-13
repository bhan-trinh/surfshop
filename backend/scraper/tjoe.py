import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def tjoe_parse_name(card: WebElement) -> str:
    PRODUCT_NAME_CLASS = (
        "SearchResultCard_searchResultCard__titleLink__2nz6x"
    )

    return card.find_element(By.CSS_SELECTOR, f".{PRODUCT_NAME_CLASS}").text


def tjoe_parse_price(card: WebElement) -> float | None:
    PRODUCT_PRICE_CLASS = "ProductPrice_productPrice__price__3-50j"

    try:
        raw_price = card.find_element(By.CSS_SELECTOR, f".{PRODUCT_PRICE_CLASS}").text

    except Exception:
        print("FAILED:", type(e).__name__, e)
        print("CARD HTML:")
        print(card.get_attribute("outerHTML")[:3000])
        return None

    return extract_price(raw_price)


def extract_price(raw_str: str):
    match = re.search(r"\$(\d\.\d\d)", raw_str)
    return float(match.group(1)) if match else None


def tjoe_parse_amount(card: WebElement) -> float | None:
    PRODUCT_AMOUNT_CLASS = "ProductPrice_productPrice__unit__2jvkA"

    raw_amount = card.find_element(By.CSS_SELECTOR, f".{PRODUCT_AMOUNT_CLASS}").text

    amount, _ = extract_amount_and_unit(raw_amount)

    return amount


def tjoe_parse_unit(card: WebElement) -> str | None:
    PRODUCT_AMOUNT_CLASS = "ProductPrice_productPrice__unit__2jvkA"

    raw_amount = card.find_element(By.CSS_SELECTOR, f".{PRODUCT_AMOUNT_CLASS}").text

    _, unit = extract_amount_and_unit(raw_amount)

    return unit


def extract_amount_and_unit(raw_str: str):
    match = re.search(r"\/(?P<amount>\d*[.]?\d*)\s?(x )?(?P<unit>.*)", raw_str)
    return (
        (float(match.group("amount")), match.group("unit")) if match else (None, None)
    )
