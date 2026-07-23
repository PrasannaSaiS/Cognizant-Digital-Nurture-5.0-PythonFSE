"""
Hands-On 6 - Task 1: Organise Scripts into pytest Tests

Run with:
    pytest test_playground.py -v
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


# Step 42: test_simple_form_submission(driver)
def test_simple_form_submission(driver):
    driver.get(BASE_URL + "simple-form-demo/")

    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys("Hello Selenium")
    driver.find_element(By.CSS_SELECTOR, "#single-input button").click()

    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed_message.text == "Hello Selenium"


# Step 43: test_checkbox_demo(driver)
def test_checkbox_demo(driver):
    driver.get(BASE_URL + "checkbox-demo/")

    first_checkbox = driver.find_element(By.ID, "isAgeSelected")
    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False

# Step 44: run `pytest test_playground.py -v` and verify both tests pass,
# each with its own freshly set-up and torn-down driver instance.
