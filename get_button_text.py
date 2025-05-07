from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Launch browser
driver = webdriver.Chrome(options=options)

try:
    url = "https://franasal-movie-picker-movie-picker-qhlofh.streamlit.app/"
    driver.get(url)

    # Wait for the page to load (adjust time as needed)
    driver.implicitly_wait(10)

    # Find all buttons and print their text
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, button in enumerate(buttons):
        print(f"Button {i+1}: {button.text}")

finally:
    driver.quit()
