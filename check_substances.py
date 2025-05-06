from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://vivid-hamburg.streamlit.app"

# Configure Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    print(f"Visiting {url}")
    driver.get(url)
    time.sleep(5)  # wait for JS to load

    page = driver.page_source.lower()
    if "take this page online" in page:
        print("App is sleeping. Trying to wake it...")
        try:
            btn = driver.find_element(By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'Yes, get this app back up!')]")
            btn.click()
            print("Clicked wake-up button.")
        except Exception as e:
            print(f"Failed to click the button: {e}")
    else:
        print("App is already online.")
finally:
    driver.quit()
