
from selenium import webdriver


def get_driver():
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)

    return driver

driver = get_driver()