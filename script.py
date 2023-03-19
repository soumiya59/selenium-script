## IMPORTS ##
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote
from re import fullmatch
import time
# Driver Managers
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager

"""
Below the script is configured set to use chrome. Be sure to change it according to the browser you use.
"""
browser = "Chrome"

## INPUT ##
print("\n")
print("Write recipient phone number in format +[Country Code][phone number]:")
phone_no = str(input())
print("\nWrite message:")
message = str(input())

## HELPERS ##
def modify_number(phone_no):
    phone_no = phone_no.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return phone_no

def validate_number(phone_no):
    def check_number(number):
        return "+" in number or "_" in number

    if not check_number(number=phone_no):
        raise Exception("Country Code Missing in Phone Number!")

    if not fullmatch(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", phone_no):
        raise Exception("Invalid Phone Number.")
    return True

def set_browser(browser):
    install = lambda dm : dm.install()
    try:
        if (browser == "Edge"):
            bm = EdgeChromiumDriverManager()
            return webdriver.Edge(service=Service(install(bm)))
        elif (browser == "Chrome"):
            bm = ChromeDriverManager()
            return webdriver.Chrome(service=Service(install(bm)))
        elif (browser == "Firefox"):
            bm = GeckoDriverManager()
            return webdriver.Firefox(service=Service(install(bm)))
        elif (browser == "Opera"):
            bm = OperaDriverManager()
            return webdriver.Opera(service=Service(install(bm)))
    except:
        raise Exception("Browser not found")

## SCRIPT ##
phone_no = modify_number(phone_no)
if (validate_number(phone_no)):
    driver = set_browser(browser)
    # uncomment the for loop to send resend a message multiple times
    # for i in range(2):
    site = f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}"
    driver.get(site)
    element = lambda d : d.find_elements(by=By.XPATH, value="//div//button/span[@data-icon='send']")
    loaded = WebDriverWait(driver, 1000).until(method=element, message="User never signed in")
    driver.implicitly_wait(10)
    send = element(driver)[0]
    send.click()
    time.sleep(3) 
    driver.close()
