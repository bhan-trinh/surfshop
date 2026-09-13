from backend.scrape.scrape_by_product_search import scrape_by_product_search
import sys

"""
NOTE:
- Make a game with an ecosystem (e.g. Rain World)
- Make a game with an inventory and item system (e.g. Stardew Valley)
"""

def main():
    keyword = sys.argv[1]
    products = scrape_by_product_search(keyword, "Tjoe")
    
    for product in products:
        print(product)
        print("==========================")
        
if __name__ == "__main__":
    main()
