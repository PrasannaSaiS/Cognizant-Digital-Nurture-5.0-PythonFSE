"""
Hands-On 7 - Task 2, Steps 55-58
Full POM-based test suite. Zero driver.find_element calls appear in this
file - all interactions go through Page Object methods. This file only
contains navigation and ASSERTIONS ("what should happen"); the "how to
make it happen" logic lives entirely in the pages/ classes.

Run with:
    pytest tests/ -v --html=report.html --self-contained-html
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


# --- Step 55 ---
def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo/")
    page.enter_message("Hello Selenium")
    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


# --- Step 56 (checkbox) ---
def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo/")

    page.check_option(0)
    assert page.is_option_checked(0) is True

    page.uncheck_option(0)
    assert page.is_option_checked(0) is False


# --- Step 56 (dropdown) ---
def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo/")

    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday"


# --- Step 57 ---
def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo/")

    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="221B Baker Street, London",
    )
    page.submit_form()

    assert "successfully" in page.get_success_message().lower()


"""
Step 59: Maintenance comment

If the Submit button's ID changed from 'submit' to 'btn-submit' in a FLAT
(non-POM) script, every single test file that contains a hardcoded
`driver.find_element(By.ID, 'submit')` call would break simultaneously -
and a developer would have to hunt through every test file individually,
find each occurrence, and fix them one by one. In a suite with dozens of
tests referencing the same button, this could mean updating 15-20
different lines across many files, with a high risk of missing one.

With POM, the SUBMIT_BUTTON locator tuple is defined in exactly ONE place
- inside the relevant Page Object class (e.g., SimpleFormPage.SUBMIT_BUTTON
or InputFormPage.SUBMIT_BUTTON). When the ID changes, only that single
class-level constant needs to be updated. Every test that calls
page.click_submit() or page.submit_form() automatically picks up the fix
with zero changes to the test files themselves. This is the core
maintainability benefit of the Page Object Model.
"""
