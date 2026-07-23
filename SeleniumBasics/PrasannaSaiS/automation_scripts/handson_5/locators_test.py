"""
Hands-On 5 - Task 1: Locator Strategies - From Simple to Robust

Target: Simple Form Demo page and Checkbox Demo page on
https://www.lambdatest.com/selenium-playground/

"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "hands_on_4"))
from setup_test import build_driver  
from selenium.webdriver.common.by import By  

SIMPLE_FORM_URL = "https://www.lambdatest.com/selenium-playground/simple-form-demo"
CHECKBOX_URL = "https://www.lambdatest.com/selenium-playground/checkbox-demo"


def test_all_locator_strategies_find_message_input():
    """Step 32: locate the same element with 6 different strategies."""
    driver = build_driver(headless=True)
    try:
        driver.get(SIMPLE_FORM_URL)

        by_id = driver.find_element(By.ID, "user-message")
        by_name = driver.find_element(By.NAME, "message")
        by_class = driver.find_element(By.CLASS_NAME, "form-control")
        by_tag = driver.find_element(By.TAG_NAME, "input")
        by_xpath_absolute = driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[2]/form/div[1]/input"
        )
        by_xpath_relative = driver.find_element(
            By.XPATH, "//input[@id='user-message']"
        )

        for element in (
            by_id,
            by_name,
            by_class,
            by_tag,
            by_xpath_absolute,
            by_xpath_relative,
        ):
            assert element.get_attribute("id") == "user-message"

        print("All 6 locator strategies found the message input successfully.")
    finally:
        driver.quit()


def test_css_selectors_for_message_input():
    """Step 33: three different CSS selectors for the same element."""
    driver = build_driver(headless=True)
    try:
        driver.get(SIMPLE_FORM_URL)

        by_css_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        by_css_attribute = driver.find_element(
            By.CSS_SELECTOR, "input[name='message']"
        )
        by_css_parent_child = driver.find_element(
            By.CSS_SELECTOR, "div.form-group > input#user-message"
        )

        for element in (by_css_id, by_css_attribute, by_css_parent_child):
            assert element.get_attribute("id") == "user-message"

        print("All 3 CSS selectors found the message input successfully.")
    finally:
        driver.quit()


def test_xpath_text_functions_on_checkboxes():
    """Step 34: XPath text() and contains() for checkbox labels."""
    driver = build_driver(headless=True)
    try:
        driver.get(CHECKBOX_URL)

        exact_match = driver.find_elements(By.XPATH, "//label[text()='Option 1']")
        assert len(exact_match) >= 1

        contains_match = driver.find_elements(
            By.XPATH, "//label[contains(text(),'Option')]"
        )
        assert len(contains_match) >= 1

        print(f"Found {len(contains_match)} labels containing 'Option'.")
    finally:
        driver.quit()


"""
Step 35: Ranking locator strategies
"""

if __name__ == "__main__":
    test_all_locator_strategies_find_message_input()
    test_css_selectors_for_message_input()
    test_xpath_text_functions_on_checkboxes()
