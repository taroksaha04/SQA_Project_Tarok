import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time  # Import the time module

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="session")
def driver():
    # Set up the WebDriver using the Service class
    service = Service('./drivers/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Open HRM
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # Maximize the browser window
    driver.maximize_window()
    # Wait for some time to observe the result
    # time.sleep(10)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h5[normalize-space()='Login']"))
    )

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys("Admin")
    password_field.send_keys("admin123")

    # Locate the login button and click it
    login_button = driver.find_element(By.XPATH, "//button[normalize-space()='Login']")
    login_button.click()

    # Return the driver to be reused across tests
    yield driver

    # Teardown: Close the driver session after all tests are done
    driver.quit()
