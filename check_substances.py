import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

# Setup headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

url = "https://vivid-hamburg.streamlit.app"
status_msg = ""

try:
    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source.lower()

    if "take this page online" in page_source:
        btn = driver.find_element(By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'take this page online')]")
        btn.click()
        status_msg = "Streamlit app was asleep — triggered wake-up button."
    else:
        # App is online — extract page content (e.g., first visible <div> or heading)
        content_div = driver.find_element(By.CSS_SELECTOR, "body").text
        preview = content_div.strip().split('\n')[0:5]  # first 5 lines
        status_msg = "Streamlit app is online. Here's a preview:\n\n" + "\n".join(preview)

finally:
    driver.quit()
    send_telegram_message(status_msg)
