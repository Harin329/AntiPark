from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from dotenv import load_dotenv
import os

load_dotenv()

def payParking():
    ZONE_ID = 5630
    TIME = "1 Hour"
    COST = "$4.00"
    sleepTime = 1

    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')

    # Visit https://parking.honkmobile.com/hourly/zones/ZONE_ID
    options = Options()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
    # use less cpu
    options.add_argument("disable-infobars")
    options.add_argument("--disable-crash-reporter");
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--aggressive-cache-discard")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-offline-load-stale-cache")
    options.add_argument("--disk-cache-size=0")
    driver = webdriver.Firefox(options=options)
    try:
        driver.get("https://parking.honkmobile.com/hourly/zones/" + str(ZONE_ID))
        time.sleep(sleepTime)

        print(driver.find_element(By.TAG_NAME, "body").text)
        
        # Click on 1 Hour option
        elem = driver.find_element(By.XPATH, "//*[text()='" + str(TIME) + "']")
        elem.click()
        time.sleep(sleepTime)

        # If login is needed
        loginElement = driver.find_element(By.XPATH, "//*[text()='Log In']")
        signupElement = driver.find_element(By.XPATH, "//*[text()='Sign Up']")

        if loginElement.is_displayed() and signupElement.is_displayed():
            loginElement.click()
            time.sleep(sleepTime)
            loginWithEmailElement = driver.find_element(By.XPATH, "//*[contains(text(),'Email')]")
            loginWithEmailElement.click()
            emailInput = driver.find_element(By.XPATH, "//*[@type='email']")
            emailInput.send_keys(EMAIL)
            passwordInput = driver.find_element(By.XPATH, "//*[@type='password']")
            passwordInput.send_keys(PASSWORD)
            passwordInput.send_keys(Keys.RETURN)
            time.sleep(sleepTime)

        # Debug utility
        # driver.get_screenshot_as_file("screenshot.png")

        # Click Pay & Park
        payAndParkElement = driver.find_element(By.XPATH, "//*[text()='Pay " + str(COST) + " & Park']")
        payAndParkElement.click()
        time.sleep(sleepTime)
        isSuccess = "Please select a different payment method." in driver.page_source
        driver.close()
        return isSuccess
    except Exception as e:
        print(e)
        driver.close()
        return False
