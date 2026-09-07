from backend import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def scroll_to_load():
    try:
        LOAD_MORE_BUTTON = driver.find_element(By.CLASS_NAME, "e-1o3e8yi")
        ActionChains(driver).scroll_to_element(LOAD_MORE_BUTTON).perform()
    except Exception as e:
        print("ERROR: Can't find Load More button.")
        print(e)


def close_address_panel():
    """Closes panel confirming delivery address."""
    try:
        CONFIRM_ADDR_CLASS = "e-182rjqr"
        driver.find_element(By.CLASS_NAME, CONFIRM_ADDR_CLASS).click()
    except Exception as e:
        print("ERROR: Can't find Delivery Address Confirm button.")
        print(e)


def close_cookie_panel():
    try:
        COOKIE_REJECT_ID = "onetrust-reject-all-handler"
        driver.find_element(By.ID, COOKIE_REJECT_ID).click()
    except Exception as e:
        print("ERROR: Can't find Cookie Reject button.")
        print(e)
