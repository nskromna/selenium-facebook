import time
import urllib
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--start-fullscreen")
# options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("http://www.google.com")

accept_cookies = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='tHlp8d']"))
        )
accept_cookies.click()

search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
        )
search_input.send_keys("dog")
search_input.send_keys(Keys.RETURN)



graphics_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Grafika"))
        )
graphics_btn.click()

image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@class='rg_i Q4LuWd']"))
    )
with open("dog.png", 'wb') as file:
    file.write(image.screenshot_as_png)

downloads_path = str(Path.home() / "Downloads")
urllib.request.urlretrieve(image.get_attribute("src"),f"{downloads_path}/dog.jpg")

# search for site
# search_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
#         )
# search_input.send_keys("facebook")
# search_input.send_keys(Keys.RETURN)

# # click on site's link
# search_results_titles = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, "//div[@id='rso']//cite"))
#         )

# for title in search_results_titles:
#     if "facebook.com" in title.text:
#         title.click()
#         break

time.sleep(3)
driver.quit()