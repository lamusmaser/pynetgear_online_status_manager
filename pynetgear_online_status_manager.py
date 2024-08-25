import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RouterAutomation:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.driver = self._setup_driver()

    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service()
        return webdriver.Chrome(service=service, options=chrome_options)

    def login(self):
        self.driver.get(f"http://{self.ip}")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "userId"))
        )
        self.driver.find_element(By.ID, "userId").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    def wait_for_page_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "loc1"))
        )

    def check_wifi_status(self, element_id):
        loc_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, element_id))
        )
        loc_status_class = loc_element.get_attribute("class").split()[-1]
        if loc_status_class == "disable":
            return "Disabled"
        elif loc_status_class == "gray":
            return "No Connection"
        else:
            return "Connected"

    def get_2g_status(self):
        return self.check_wifi_status("loc2")

    def get_5g_status(self):
        return self.check_wifi_status("loc3")

    def navigate_to_wifi_settings(self):
        self.driver.find_element(By.ID, "wifiSettings").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "general"))
        )

    def toggle_2g(self):
        self.driver.find_element(By.ID, "enableAp").click()

    def toggle_5g(self):
        self.driver.find_element(By.ID, "enableAp5g").click()

    def save_settings(self):
        self.driver.find_element(By.ID, "saveBt1").click()
        time.sleep(5)

    def navigate_to_status_page(self):
        self.driver.find_element(By.ID, "status").click()
        self.wait_for_page_load()

    def navigate_to_restart_page(self):
        self.driver.find_element(By.ID, "otherSettings").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "restartBt"))
        )

    def restart_router(self):
        self.driver.find_element(By.ID, "restartBt").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "restartYesBt"))
        )
        self.driver.find_element(By.ID, "restartYesBt").click()
        time.sleep(150)

    def close(self):
        self.driver.quit()

    def manage_wifi(self):
        # Get initial statuses
        self.login()
        self.wait_for_page_load()
        two_g_status = self.get_2g_status()
        five_g_status = self.get_5g_status()

        print(f"Initial 2GHz Wi-Fi Status: {two_g_status}")
        print(f"Initial 5GHz Wi-Fi Status: {five_g_status}")

        # Logic for restarting 2.4GHz or 5GHz connection
        if two_g_status != "Connected" or five_g_status != "Connected":
            self.navigate_to_wifi_settings()
            if two_g_status != "Connected":
                self.toggle_2g()
            if five_g_status != "Connected":
                self.toggle_5g()
            self.save_settings()
            self.navigate_to_status_page()

        # Optional: recheck the statuses here

        if os.getenv("ACTION").lower() == "restart":
            self.restart_router()
            self.login()
            self.wait_for_page_load()

        # Final statuses after possible changes
        two_g_status = self.get_2g_status()
        five_g_status = self.get_5g_status()
        print(f"Final 2GHz Wi-Fi Status: {two_g_status}")
        print(f"Final 5GHz Wi-Fi Status: {five_g_status}")

        self.close()


# Main execution
if __name__ == "__main__":
    router_ip = os.getenv("ROUTER_IP")
    username = os.getenv("ROUTER_USERNAME")
    password = os.getenv("ROUTER_PASSWORD")

    router_automation = RouterAutomation(router_ip, username, password)
    router_automation.manage_wifi()
