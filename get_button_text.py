import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Config
URL = "https://francisco.streamlit.app/"

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Missing Telegram credentials.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    print("Telegram status:", response.status_code)
    print("Response:", response.text)

def check_site_with_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        driver.implicitly_wait(10)

        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, button in enumerate(buttons):
            text = button.text.strip()
            print(f"Button {i+1}: {text}")
            if "get this app back up" in text.lower():
                send_telegram_message(f"Site is asleep: {text}")
                button.click()
                time.sleep(3)
                send_telegram_message("Wake-up button clicked.")
                return  # Skip rest of scraping if site was asleep

        # If no sleep message, scrape site content
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text().strip()[:500]
        send_telegram_message("Site is online:\n" + page_text)

    except Exception as e:
        send_telegram_message(f"Error during site check: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_site_with_selenium()
