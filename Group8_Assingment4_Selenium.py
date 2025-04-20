from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)
response_times = {}

def measure_response(name, action_func, wait_condition=None):
    start = time.time()
    action_func()
    if wait_condition:
        wait.until(wait_condition)
    end = time.time()
    duration = round(end - start, 2)
    response_times[name] = duration
    print(f"{name} response time: {duration} sec")

def search_action():
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.clear()
    search_box.send_keys("wireless headphones")
    driver.find_element(By.ID, "nav-search-submit-button").click()

measure_response(
    "Homepage Load",
    lambda: driver.get("https://www.amazon.in"),
    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
)

measure_response(
    "Search 'wireless headphones'",
    search_action,
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
)

measure_response(
    "Sort by Price: Low to High",
    lambda: Select(driver.find_element(By.ID, "s-result-sort-select")).select_by_visible_text("Price: Low to High"),
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
)

items = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
name1, price1 = "", ""
for item in items:
    try:
        name1 = item.find_element(By.CSS_SELECTOR, "h2 span").text
        price1 = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        break
    except:
        continue
print(f"Lowest Priced Item: {name1} - ₹{price1}")

measure_response(
    "Sort by Avg. Customer Review",
    lambda: Select(driver.find_element(By.ID, "s-result-sort-select")).select_by_visible_text("Avg. Customer Review"),
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
)

items = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
name2, price2, product_link = "", "", ""
for item in items:
    try:
        name2 = item.find_element(By.CSS_SELECTOR, "h2 span").text
        price2 = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        product_link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        break
    except:
        continue
print(f"Top-Rated Item: {name2} - ₹{price2}")

def add_to_cart():
    driver.get(product_link)
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button"))).click()

measure_response(
    "Add to Cart",
    add_to_cart,
    EC.presence_of_element_located((By.ID, "attach-sidesheet-checkout-button-announce"))  # Wait for cart button to confirm
)
print("Item added to cart")

print("\nSummary of Response Times:")
for step, duration in response_times.items():
    print(f"{step}: {duration} sec")

driver.quit()