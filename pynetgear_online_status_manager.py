import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Load environment variables
router_ip = os.getenv("ROUTER_IP")
router_username = os.getenv("ROUTER_USERNAME")
router_password = os.getenv("ROUTER_PASSWORD")

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver with Selenium Manager handling chromedriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL to the router login page
url = f"http://{router_ip}/status.htm"

try:
    # Open the router login page
    driver.get(url)

    # Locate the username and password fields and enter credentials
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "login")

    username_input.send_keys(router_username)
    password_input.send_keys(router_password)
    login_button.click()

    # Check the page contents for 2GHz and 5GHz Wi-Fi statuses
    page_source = driver.page_source

    # Check for 2GHz status
    link_status_2g = None
    if "link_status_2g" in page_source:
        link_status_2g = driver.find_element(By.ID, "link_status_2g").text

    # Check for 5GHz status
    link_status_5g = None
    if "link_status_5g" in page_source:
        link_status_5g = driver.find_element(By.ID, "link_status_5g").text

    print(f"2GHz Wi-Fi Enabled: {link_status_2g is not None}")
    print(f"5GHz Wi-Fi Enabled: {link_status_5g is not None}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver session
    driver.quit()
