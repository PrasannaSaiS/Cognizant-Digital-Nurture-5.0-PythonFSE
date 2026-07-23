"""
Hands-On 7 - Task 1, Steps 51-52
SimpleFormPage: encapsulates all locators and actions for the
Simple Form Demo page. No assertions live here - only actions and
value getters.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    # Class-level locator tuples - single source of truth for this page
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#single-input button")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text: str):
        message_box = self.wait_for_element(self.MESSAGE_INPUT)
        message_box.clear()
        message_box.send_keys(text)

    def click_submit(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self) -> str:
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
