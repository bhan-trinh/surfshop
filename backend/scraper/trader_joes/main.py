from backend.scraper.base import Scraper


class TraderJoesScraper(Scraper):
    PRODUCT_NAME_CLASS = "SearchResultCard_searchResultCard__titleLink__2nz6x"
    PRODUCT_PRICE_CLASS = "ProductPrice_productPrice__price__3-50j"
    PRODUCT_AMOUNT_CLASS = "ProductPrice_productPrice__unit__2jvkA"
    
    def __init__(self):
        super().__init__(
            store="Trader Joe's",
            product_name_class=self.PRODUCT_NAME_CLASS,
            product_price_class=self.PRODUCT_PRICE_CLASS,
            product_amount_class=self.PRODUCT_AMOUNT_CLASS
        )