import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

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
    driver.implicitly_wait(5)
    yield driver  # This returns the driver to the test

    # Teardown: Close the browser (this is the teardown)
    driver.quit() # Ensures that the browser is closed after the test

def test_alert(driver):
    # Open page
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    print("Page Loaded, the title is:", driver.title)

    alert_button = driver.find_element(By.XPATH, "//button[normalize-space()='Click for JS Alert']")
    alert_button.click()
    print("Button clicked")

    try:
        # input("Waiting for alert to appear...")
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert

        print("Alert Text:", alert.text)
        alert.accept()

    except NoSuchElementException:
        print("Element not found")
        assert False
    except TimeoutException as e:
        print("Timeout occurred waiting for alert: ", str(e))
        assert False
    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")
        assert False

def test_windows(driver):
    # Open page
    driver.get("https://the-internet.herokuapp.com/windows")
    print("Windows Page Loaded, the title is:", driver.title)

    windows_button = driver.find_element(By.XPATH, "//a[normalize-space()='Click Here']")
    windows_button.click()

    # Click on the link that opens a new window
    # driver.find_element_by_link_text("Click Here").click()
    print("Windows button clicked")

    # Get all window handles
    windows = driver.window_handles

    # Switch to the new window
    driver.switch_to.window(windows[1])

    try:
        print("Finding content in newly opened window")
        content = driver.find_element(By.XPATH, "//h3[normalize-space()='New Window']")
        print("Content found, content is:", content.text)
        assert "New Window" in content.text, "Opening new window failed"
    except NoSuchElementException:
        print("Element not found to open new window")
        assert False
    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")
        assert False

def test_frame(driver):
    # Open page
    driver.get("https://demoqa.com/frames")
    print("Frame Page Loaded, the title is:", driver.title)

    large_frame = driver.find_element(By.ID, "frame1")
    small_frame = driver.find_element(By.ID, "frame2")

    print("Frames are identified", large_frame, small_frame)

    # Switching to the large frame
    driver.switch_to.frame(large_frame)
    # Getting content from the large frame
    content_in_large_frame = driver.find_element(By.ID, "sampleHeading")
    print("Content in large frame: ", content_in_large_frame.text)

    # Switch back to the main document (default content)
    driver.switch_to.default_content()

    # Switching to the small frame
    driver.switch_to.frame(small_frame)
    # Getting content from the small frame
    content_in_small_frame = driver.find_element(By.ID, "sampleHeading")
    print("Content in small frame: ", content_in_small_frame.text)

    # Switch back to the main document (default content)
    driver.switch_to.default_content()

    try:
        print("Finding content in default frame")
        content = driver.find_element(By.XPATH, "//h1[normalize-space()='Frames']")
        print("Content found, content is:", content.text)
        assert "Frames" in content.text, "Navigating to the default frame is failed"
    except NoSuchElementException:
        print("No frame is found")
        assert False
    except WebDriverException as e:
        print(f"WebDriver exception occurred: {e}")
        assert False