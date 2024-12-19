import json
import os
import pickle
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time  # Import the time module

from selenium.webdriver.support.wait import WebDriverWait

# Creating screenshot folder utility
def create_screenshot_folder(test_name):
    base_screenshot_folder = 'screenshots'

    # Create the base screenshot folder if not exists
    if not os.path.exists(base_screenshot_folder):
        os.makedirs(base_screenshot_folder)

    # Create a folder for the specific test
    test_case_folder = os.path.join(base_screenshot_folder, test_name)
    if not os.path.exists(test_case_folder):
        os.makedirs(test_case_folder)

    return test_case_folder

# Pytest fixture to handle WebDriver setup and teardown
@pytest.fixture(scope="module")
def driver():
    # Set up the WebDriver using the Service class
    service = Service('./drivers/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    #driver.implicitly_wait(10)
    yield driver  # This returns the driver to the test

    # Teardown: Close the browser (this is the teardown)
    driver.quit() # Ensures that the browser is closed after the test

@pytest.mark.mark1
def test_01_login(driver):
    print("Starting the test.")
    folder = create_screenshot_folder('login_test')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Open HRM
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # Maximize the browser window
    driver.maximize_window()
    print("Navigated to OrangeHRM login page. Title: ", driver.title)

    # Wait for some time to observe the result
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h5[normalize-space()='Login']"))
    )
    try:
        # Locate the username and password fields and input login credentials
        print("Trying to locate username and password fields.")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
    except NoSuchElementException:
        # Take Screenshot if login form not found
        screenshot_path = os.path.join(folder, f'field_unavailable_{timestamp}.png')
        driver.save_screenshot(screenshot_path)

        raise AssertionError("Test failed: Username and password fields are not available.")

    # Enter the login credentials
    print("Entering the username and password.")
    username_field.send_keys("Admin")
    password_field.send_keys("admin123")

    # Locate the login button and click it
    login_button = driver.find_element(By.XPATH, "//button[normalize-space()='Login']")
    login_button.click()

    # Check for a failed login indicator
    try:
        error_message = driver.find_element(By.XPATH, "(//p[@class='oxd-text oxd-text--p oxd-alert-content-text'])[1]")
        print(error_message.text)
        if error_message.text== "Invalid credentials":
            # Take Screenshot after login failed
            screenshot_path = os.path.join(folder, f'invalid_cred_{timestamp}.png')
            driver.save_screenshot(screenshot_path)
            raise AssertionError("Login failed, username and/or password is invalid")

    except NoSuchElementException:
        # Wait for some time to observe the result
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Dashboard']"))
        )

        # Take Screenshot after login successful
        screenshot_path = os.path.join(folder, f'dashboard_{timestamp}.png')
        driver.save_screenshot(screenshot_path)

        browser_title = driver.title
        url = driver.current_url

        # Save cookies to a file after login
        with open("cookies.pkl", "wb") as file:
            pickle.dump(driver.get_cookies(), file)

        print("Login successful and cookies saved. Page title: ", browser_title)


        # # Capture local storage data after login
        # local_storage = driver.execute_script("return window.localStorage;")
        #
        # # Set local storage data before running the next test
        # for key, value in local_storage.items():
        #     value_json = json.dumps(value)  # Properly escapes the value
        #     driver.execute_script(f"window.localStorage.setItem('{key}', {value_json});")
        #
        # # Save local storage data to a file
        # with open("local_storage.pkl", "wb") as f:
        #     pickle.dump(local_storage, f)


        # Assert that login was successful by checking the title, URL, or page content
        assert "dashboard" in url.lower(), "Dashboard is not found in url"
        # assert "Logged in successfullyyyy" in success_message.text, "Dashboard not found"
        # assert "EMS : Administer/Dashboard" in browser_title, "Dashboard not found"

    except TimeoutException as e:
        print("Timeout occurred waiting for login: ", str(e))
        # Take Screenshot after login failed
        screenshot_path = os.path.join(folder, f'timeout_{timestamp}.png')
        driver.save_screenshot(screenshot_path)
        assert False
