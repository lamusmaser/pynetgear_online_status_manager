import os
import time

from pynetgear_enhanced import Netgear

# Fetch router credentials from environment variables
ROUTER_USERNAME = os.getenv("ROUTER_USERNAME", "admin")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD", "password")
ROUTER_IP = os.getenv("ROUTER_IP", "192.168.1.1")  # Default Netgear router IP


def check_and_repair_wifi(netgear):
    # Get WiFi status
    wifi_status = netgear.get_wifi_info()

    # Extract the status of 2.4 GHz and 5 GHz
    is_24ghz_online = wifi_status["2.4GHz"]["status"]
    is_5ghz_online = wifi_status["5GHz"]["status"]

    # Store the states before attempting repair
    initial_24ghz_online = is_24ghz_online
    initial_5ghz_online = is_5ghz_online

    # Disable/Enable 2.4 GHz if it's offline
    if not initial_24ghz_online and initial_5ghz_online:
        print("2.4 GHz is offline. Attempting to repair...")
        netgear.set_wifi_2g(enable=False)
        time.sleep(15)
        netgear.set_wifi_2g(enable=True)
        time.sleep(15)
        is_24ghz_online = netgear.get_wifi_info()["2.4GHz"]["status"]

    # Disable/Enable 5 GHz if it's offline
    if not initial_5ghz_online and initial_24ghz_online:
        print("5 GHz is offline. Attempting to repair...")
        netgear.set_wifi_5g(enable=False)
        time.sleep(15)
        netgear.set_wifi_5g(enable=True)
        time.sleep(15)
        is_5ghz_online = netgear.get_wifi_info()["5GHz"]["status"]

    # Check the final status after repair attempts
    if not initial_24ghz_online and not initial_5ghz_online:
        print("Both 2.4 GHz and 5 GHz are offline. Rebooting router...")
        netgear.reboot()
    elif not is_24ghz_online or not is_5ghz_online:
        print("One of the WiFi bands is still offline. Rebooting router...")
        netgear.reboot()
    else:
        print("Both 2.4 GHz and 5 GHz are online.")


def main():
    # Connect to the router
    netgear = Netgear(
        password=ROUTER_PASSWORD, host=ROUTER_IP, user=ROUTER_USERNAME
    )

    if not netgear.login():
        print(
            "Failed to connect to the router. Please check your credentials."
        )
        return

    try:
        check_and_repair_wifi(netgear)
    finally:
        netgear.logout()


if __name__ == "__main__":
    main()
