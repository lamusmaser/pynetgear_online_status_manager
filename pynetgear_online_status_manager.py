import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RouterManager:
    def __init__(self, driver, router_ip, username, password):
        self.driver = driver
        self.router_ip = router_ip
        self.username = username
        self.password = password

    def login(self):
        print(f"Attempting login on {self.router_ip}.")
        self.driver.get(f"http://{self.router_ip}")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#loginBt"))
        )
        self.driver.find_element(By.ID, "userId").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.loc1"))
        )
        print(f"Status page successfully loaded. Login deemed successful.")

    def get_wifi_info(self):
        print(f"Getting active band information...")
        status = {}
        status["2.4GHz"] = self._get_band_status("loc2")
        status["5GHz"] = self._get_band_status("loc3")
        print(f"Current status: {status}")
        return status

    def _get_band_status(self, locator):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"div.{locator}"))
        )
        additional_class = element.get_attribute("class").split()[1]
        if additional_class == "disable":
            return "Disabled"
        elif additional_class == "gray":
            return "No Connection"
        else:
            return "Connected"

    def set_wifi(self, band, enable):
        print(f"Setting {band} band to {'en' if enable else 'dis'}abled.")
        self.navigate_to("a#wifiSettings", "h2#general", "/wifiSettings.htm")
        toggle_selector = (
            "input#enableAp" if band == "2.4GHz" else "input#enableAp5g"
        )
        toggle = self.driver.find_element(By.CSS_SELECTOR, toggle_selector)
        if enable and not toggle.is_selected():
            toggle.click()
        elif not enable and toggle.is_selected():
            toggle.click()
        self.driver.find_element(By.CSS_SELECTOR, "input#saveBt1").click()
        time.sleep(5)
        print("Assuming setting is success. Returning to status page.")
        self.navigate_to("a#status", "div.loc1", "/status.htm")

    def reboot(self):
        reboot_wait = 150
        print(
            f"Determined that a reboot action needs to occur for the system. Navigating to internal resource to restart system."
        )
        self.navigate_to(
            "a#otherSettings", "a#restartBt", "/backUpSettings.htm"
        )
        self.driver.find_element(By.CSS_SELECTOR, "a#restartBt").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input#restartYesBt")
            )
        ).click()
        print(
            f"Clicked buttons. Waiting for {reboot_wait} seconds before checking current status."
        )
        time.sleep(reboot_wait)
        print(f"Attempting to login after reboot.")
        self.login()

    def navigate_to(self, click_selector, wait_selector, url):
        print(f"Attempting to navigate to new page: {url}")
        self.driver.find_element(By.CSS_SELECTOR, click_selector).click()
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
        )

    def repair_wifi(self):
        initial_status = self.get_wifi_info()
        is_24ghz_online = initial_status["2.4GHz"] == "Connected"
        is_5ghz_online = initial_status["5GHz"] == "Connected"

        print("Attempting repair of wifi connectivity.")
        if not is_24ghz_online and is_5ghz_online:
            print("2.4 GHz is offline. Attempting to repair...")
            self.set_wifi("2.4GHz", enable=False)
            time.sleep(15)
            self.set_wifi("2.4GHz", enable=True)
            time.sleep(15)
            is_24ghz_online = self.get_wifi_info()["2.4GHz"] == "Connected"

        if not is_5ghz_online and is_24ghz_online:
            print("5 GHz is offline. Attempting to repair...")
            self.set_wifi("5GHz", enable=False)
            time.sleep(15)
            self.set_wifi("5GHz", enable=True)
            time.sleep(15)
            is_5ghz_online = self.get_wifi_info()["5GHz"] == "Connected"

        if not is_24ghz_online and not is_5ghz_online:
            print("Both 2.4 GHz and 5 GHz are offline. Rebooting router...")
            self.reboot()
        elif not is_24ghz_online or not is_5ghz_online:
            print(
                "One of the WiFi bands is still offline. Rebooting router..."
            )
            self.reboot()
        else:
            print("Both 2.4 GHz and 5 GHz are online.")


def main():
    # Retrieve credentials and IP from environment variables
    router_ip = os.getenv("ROUTER_IP")
    username = os.getenv("ROUTER_USERNAME")
    password = os.getenv("ROUTER_PASSWORD")

    # Check if the environment variables are set
    if not router_ip or not username or not password:
        raise ValueError(
            "Please set the ROUTER_IP, ROUTER_USERNAME, and ROUTER_PASSWORD environment variables."
        )

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    netgear = RouterManager(driver, router_ip, username, password)

    try:
        netgear.login()
        netgear.repair_wifi()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
