from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
from pathlib import Path

login = input("Facebook login: ")
password =  input("Facebook password: ")
friend_name = input("Friend's name and surname: ")
facebook_account_id = input("Friend's account ID: ")

options = Options()
options.add_argument("--start-fullscreen")
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("http://www.facebook.com")

# handle COOKIES
accept_cookies = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='tHlp8d']"))
        )
accept_cookies.click()

# search for site
search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='q']"))
        )
search_input.send_keys("facebook")
search_input.send_keys(Keys.RETURN)

# click on site's link
search_results_titles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='rso']//cite"))
        )

for title in search_results_titles:
    if "facebook.com" in title.text:
        title.click()
        break

# handle COOKIES
accept_cookies_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-cookiebanner='accept_only_essential_button']"))
        )
accept_cookies_btn.click()

# log into the account
login_input = driver.find_element(By.ID, "email")
password_input = driver.find_element(By.ID, "pass")
login_input.send_keys(login)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# search for a friend
search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']"))
        )
search_input.send_keys(friend_name)
search_input.send_keys(Keys.RETURN)

# collect results
try:
    search_results_1 = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//a[@aria-label='{friend_name}']"))
            )
except:
    pass

try:
    search_results_2 = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.LINK_TEXT, f"{friend_name}"))
            )
except:
    pass

# check if results exist
if search_results_1 or search_results_2:
    search_results = search_results_1 + search_results_2
else:
    print("No matches found")
    driver.quit()

# click on correct link
for result in search_results:
    if facebook_account_id in result.get_attribute("href"):
        result.click()
        break

# go to photos section
photos_section_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@href='https://www.facebook.com/{facebook_account_id}/photos']"))
            )
photos_section_link.click()

# scroll down
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# go to photos_by section
try:
    photos_by_section_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//a[@href='https://www.facebook.com/{facebook_account_id}/photos_by']"))
                )
except:
    print("This user does not have their photos")
    driver.quit()

photos_by_section_link.click()

# click on photo
link_to_photo = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='xqtp20y x1n2onr6 xh8yej3']//div//a"))
            ).click()

# save photo
photo =  WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, "//img[@data-visualcompletion='media-vc-image']"))
            )

downloads_path = str(Path.home() / "Downloads")
urllib.request.urlretrieve(photo.get_attribute("src"), f"{downloads_path}/{facebook_account_id}.jpg")

driver.quit()