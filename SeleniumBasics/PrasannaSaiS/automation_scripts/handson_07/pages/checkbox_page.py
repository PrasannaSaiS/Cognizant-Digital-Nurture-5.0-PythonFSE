"""
Hands-On 7 - Task 1, Step 53
CheckboxPage: encapsulates locators and actions for the Checkbox Demo page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOXES = (By.CSS_SELECTOR, "ul#colorbox li input[type='checkbox']")

    def _checkbox_at(self, index: int):
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)
        return checkboxes[index]

    def check_option(self, index: int):
        box = self._checkbox_at(index)
        if not box.is_selected():
            box.click()

    def uncheck_option(self, index: int):
        box = self._checkbox_at(index)
        if box.is_selected():
            box.click()

    def is_option_checked(self, index: int) -> bool:
        return self._checkbox_at(index).is_selected()
