"""
Hands-On 6 - Task 2: Parameterisation, Reporting and Screenshot on Failure

Run with:
    pytest test_playground.py -v --html=report.html --self-contained-html
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pytest


# Step 45: parametrize the form submission test with 3 input values ->
# generates 3 separate test runs, each shown individually in the report.
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")

    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys(message)
    driver.find_element(By.CSS_SELECTOR, "#single-input button").click()

    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert displayed_message.text == message


# Carried over from Task 1, now using the base_url fixture instead of a hardcoded URL string (Step 48).
def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")

    first_checkbox = driver.find_element(By.ID, "isAgeSelected")
    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False


# Step 49: test_dropdown_selection(driver)
def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo/")

    dropdown_element = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_element)
    select.select_by_visible_text("Wednesday")

    assert select.first_selected_option.text == "Wednesday"


# Included only to demonstrate that the pytest_runtest_makereport hook in
# conftest.py correctly captures a screenshot on failure (Step 46).
def test_intentional_failure_for_screenshot_demo(driver, base_url):
    driver.get(base_url)
    assert driver.title == "This Title Does Not Exist"

# Step 47: pytest test_playground.py --html=report.html --self-contained-html
# Open report.html afterward and verify it shows test names, pass/fail
# status, and duration for all 6 tests (3 parametrized + checkbox +
# dropdown + the intentional failure demo).
