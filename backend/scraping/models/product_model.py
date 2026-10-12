class Product:
    
    def __init__(self,
    name: str,
    price: float,
    category: str | None = None,
    amount: float | None = None,
    unit: str | None = None):
        self.name = name
        self.price = price
        self.amount = amount or 0
        self.unit = unit or "N/A"
        self.category = category or "N/A"
        self.price_per_unit = self.price / self.amount 

    def __str__(self):
        return(
            f"""{self.name.upper()}\n${self.price}\n{self.amount} {self.unit}\n${self.price_per_unit:.2f}/{self.unit}""")

# # Extract main categories
# url = ""

# driver.get(url)

# time.sleep(2.5)

# category_buttons = driver.find_elements(By.CLASS_NAME, "CategoryFilter_categoryFilter__subCategoryButton__4rOWH")

# category_dict = {}

# for b in category_buttons:
#     category_dict[b.text] = {  
#         "href": b.get_attribute("href")
#     }

# # Extract subcategories
# for c, i in category_dict.items():
#     driver.get(i["href"])
#     time.sleep(2.5)
#     try:    
#         subcategory_list = driver.find_element(By.CLASS_NAME, "CategoryFilter_categoryFilter__subCategoryList__26O5o")
#     except:
#         continue

#     subcategory_buttons = subcategory_list.find_elements(By.CLASS_NAME, "CategoryFilter_categoryFilter__subCategoryButton__4rOWH")
#     subcategory_dict = {}

#     for b in subcategory_buttons:
#         subcategory_dict[b.text] = {  
#             "href": b.get_attribute("href")
#         }

#     category_dict[c]["sub"] = subcategory_dict

# products: list[Product] = []

# for c, i in category_dict.items():
#     for c_s, i_s in i["sub"].items():
#         driver.get(i_s["href"])

#         time.sleep(2.5)
#         try:    
#             product_list = driver.find_element(By.CLASS_NAME, "ProductList_productList__list__3-dGs")
#         except:
#             continue

#         product_cards = product_list.find_elements(By.CLASS_NAME, "ProductList_productList__item__1EIvq")
       
#         for p in product_cards:
#             name = p.find_element(By.CLASS_NAME, "ProductCard_card__title__301JH").text
#             price = float(p.find_element(By.CLASS_NAME, "ProductPrice_productPrice__price__3-50j").text[1:])
#             product = Product(name=name, price=price, category=c_s)
#             products.append(product)

#             print(product)
