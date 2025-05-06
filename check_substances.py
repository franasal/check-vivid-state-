import requests

def check_website():
    url = 'https://vivid-hamburg.streamlit.app'  # replace with your target site
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("Website is online.")
        else:
            print(f"Website returned status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Website is down. Error: {e}")

check_website()
