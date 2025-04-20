import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

options = UiAutomator2Options()
options.device_name = "Pixel 7"
options.udid = "2C191FDH2002PB"
options.app_package = "in.amazon.mShop.android.shopping"
options.app_activity = "com.amazon.mShop.home.HomeActivity"
options.automation_name = "UiAutomator2"
options.no_reset = True

def Time_measurement(action_function, *args, **kwargs):
    start_time = time.time()
    result = action_function(*args, **kwargs)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time, result

logger.info("Starting Connection to Appium Server")
driver = webdriver.Remote("http://localhost:4723", options=options)
wait = WebDriverWait(driver, 30)


def Searching_Function():
    logger.info(" ")
    logger.info("Searching for  wireless headphones")
    sort_start_time = time.time()
    search_bar = wait.until(EC.element_to_be_clickable(
        (By.ID, "in.amazon.mShop.android.shopping:id/chrome_search_hint_view")
    ))
    search_bar.click()
    
    search_input = wait.until(EC.element_to_be_clickable(
        (By.ID, "in.amazon.mShop.android.shopping:id/rs_search_src_text")
    ))
    search_input.send_keys("wireless headphones")

    driver.press_keycode(66)

    wait.until(EC.presence_of_element_located((By.XPATH, "//android.view.View[@resource-id='s-all-filters']")))

    sort_end_time = time.time()
    sort_time = sort_end_time - sort_start_time
    logger.info(f"Time taken to search for wireless headphones : {sort_time:} seconds")
    logger.info(" ")
    

def Low_Price_Sort():
    logger.info("Sorting by price :")
    sort_start_time = time.time()
    
    
    filter_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.view.View[@resource-id='s-all-filters']")
    ))
    filter_button.click()

    sort_by = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.view.View[@text='Sort by']")
    ))
    sort_by.click()

    price_low_to_high = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.CheckBox[@resource-id='sort/price-asc-rank']")
    ))
    price_low_to_high.click()

    show_results = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.view.View[contains(@content-desc, 'Show')]")
    ))
    
    show_results.click()

    
    sort_end_time = time.time()
    sort_time = sort_end_time - sort_start_time
    logger.info(f"Time taken to sort by Lowest price : {sort_time:} seconds")
    
    


def Rating_Price_Sort():
    logger.info(" ")
    logger.info("Sorting by highest rated item: ")
    
    sort_start_time = time.time()
    
    
    filter_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.view.View[@resource-id='s-all-filters']")
    ))
    filter_button.click()

    sort_by = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.view.View[@text='Sort by']")
    ))
    sort_by.click()

    price_rate = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.CheckBox[@resource-id='sort/review-rank']")
    ))
    price_rate.click()

    show_results = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.TextView[@text='Show 2,369 results']")
    ))
    
    show_results.click()

    sort_end_time = time.time()
    sort_time = sort_end_time - sort_start_time
    
    logger.info(f"Time taken to sort by Ratings : {sort_time:} seconds ")
    
    
    
    sort_start_time2 = time.time()
    logger.info(" ")
    logger.info("Adding to cart")
    
    show_results2 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.Button[@text='Add to cart']")
    ))
    
    show_results2.click()
    
    show_results3 = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//android.widget.TextView[@text='YUMONDEAR Bluetooth Headphones Over Ear, 80H Playtime Wireless Headphone with 3 EQ Modes, Built-in Mic, Deep Bass, HiFi Stereo Foldable Wireless Headset for iPhone PC Travel Workout Office (Pink)']")
    ))
    
    show_results3.click()
    
    
    sort_end_time2 = time.time()
    sort_time = sort_end_time2 - sort_start_time
    logger.info(f"Time taken to add to cart : {sort_time:} seconds ")
    logger.info(" ")
    
    

def App_Loadtime():
    logger.info("App load time measurement:  ")

    driver.terminate_app("in.amazon.mShop.android.shopping")
    time.sleep(2)

    start_time = time.time()
    driver.activate_app("in.amazon.mShop.android.shopping")

    wait.until(EC.presence_of_element_located(
        (By.ID, "in.amazon.mShop.android.shopping:id/chrome_search_hint_view")
    ))

    end_time = time.time()
    value=end_time - start_time
    logger.info(f"Time taken to load : {value:} seconds ")
    return end_time - start_time


try:
    Dummydict = {}
    Dummydict["app_load_time"] = App_Loadtime()
    search_time, _ = Time_measurement(Searching_Function)
    sort_navigate_time, sort_navigate_results = Time_measurement(Low_Price_Sort)
    sort_by_rating_time, sort_by_rating_results = Time_measurement(Rating_Price_Sort)
    logger.info("Test completed")

finally:
    driver.quit()