from backend.scraping.scraper.aldi.aldi import AldiScraper
from backend.scraping.scraper.base import Scraper
from backend.scraping.scraper.trader_joes.trader_joes import TraderJoesScraper

"""
NOTE:
- Make a game with an ecosystem (e.g. Rain World)
- Make a game with an inventory and item system (e.g. Stardew Valley)
"""
from backend.scraping.models.product_model import Product


def scrape_by_product_search(search_keyword: str, store: str) -> list[Product] | None:
    scraper: Scraper
    
    match store.lower():
        case "aldi":
            scraper = AldiScraper()
        case "tjoe":
            scraper = TraderJoesScraper()
        case _:
            raise ValueError(f"Invalid store: {store}")

    return scraper.scrape_by_product_search(search_keyword)
