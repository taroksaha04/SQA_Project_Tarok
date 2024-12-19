
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
import time  # Import the time module
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

def test_02_employee_creation(driver):
    print("Starting the test.")

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee")
    print("Navigated to another page. Title is", driver.title)

    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Add Employee']"))
        )

        # Locating the necessary fields and input them
        print("Locating the necessary fields and input them for adding an employee")
        first_name = driver.find_element(By.XPATH, "//input[@placeholder='First Name']")
        middle_name = driver.find_element(By.XPATH, "//input[@placeholder='Middle Name']")
        last_name = driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
        employee_id = driver.find_element(By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[2]")

        # Fill in the employee details
        first_name.send_keys("John")
        middle_name.send_keys("A")
        last_name.send_keys("Doe")
        employee_id.clear()
        #employee_id.send_keys("12345")

        print("Employee information inserted")
        # Save the new employee
        save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
        save_button.click()
        print("Save button clicked")
        # Wait for the save operation to complete
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Personal Details']"))
        )
        page_content=driver.find_element(By.XPATH, "//h6[normalize-space()='Personal Details']")
        # print(page_content.text)
        assert "Personal Details" in page_content.text, "Employee not saved"


    except NoSuchElementException:
        raise AssertionError("Test failed: Couldn't add an employee")

    