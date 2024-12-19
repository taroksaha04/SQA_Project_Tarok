import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time  # Import the time module

from selenium.webdriver.support.wait import WebDriverWait


# Pytest fixture to handle WebDriver setup and teardown
@pytest.fixture
def driver():
    # Setup: Initialize the WebDriver (this is the setup)
    # Set up the WebDriver using the Service class
    service = Service('./drivers/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    #driver.implicitly_wait(10)
    yield driver  # This returns the driver to the test

    # Teardown: Close the browser (this is the teardown)
    driver.quit() # Ensures that the browser is closed after the test

def test_login(driver):
    print("Starting the test.")

    # Open EMS
    driver.get("https://ems-test.amaderit.net/")
    # driver.get("https://www.google.com/")
    # Maximize the browser window
    driver.maximize_window()
    print("Navigated to EMS page.")
    print("Page title is:", driver.title)

    try:
        # Locate the username and password fields and input login credentials
        print("Trying to locate username and password fields.")
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.NAME, "password")

    except NoSuchElementException:
        raise AssertionError("Test failed: Username and password fields are not available.")

    # Enter the login credentials
    print("Entering the username and password.")
    username_field.send_keys("adming1")
    password_field.send_keys("12345678")

    # Locate the login button and click it
    login_button = driver.find_element(By.XPATH, "//button[normalize-space()='Sign In']")
    login_button.click()

    # Check for a failed login indicator
    try:
        error_message = driver.find_element(By.XPATH, "//div[@class='message alert alert-danger']")
        if error_message.text== "Please enter your correct username and password":
           raise AssertionError("Login failed, username and/or password is invalid")

    except NoSuchElementException:
        # Wait for some time to observe the result
        time.sleep(5)

        browser_title = driver.title
        url = driver.current_url
        # success_message = driver.find_element(By.XPATH, "//div[@class='message alert alert-success']")

        # Print the page title to the console
        print(f"Page title is after login:", browser_title)

        # Wait for user input to keep the browser open
        # input("Press Enter to continue...")

        # Assert that login was successful by checking the title, URL, or page content
        # assert "administersa" in url.lower(), "administer is not found in url"
        # assert "Logged in successfullyyyy" in success_message.text, "Dashboard not found"
        assert "EMS : Administer/Dashboard" in browser_title, "Dashboard not found"