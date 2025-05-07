import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    print("Telegram status:", response.status_code)
    print("Response:", response.text)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://franasal-movie-picker-movie-picker-qhlofh.streamlit.app/")
    driver.implicitly_wait(10)

    buttons = driver.find_elements("tag name", "button")
    for i, button in enumerate(buttons):
        print(f"Button {i+1}: {button.text}")
        if button.text:
            send_telegram_message(button.text)
finally:
    driver.quit()
