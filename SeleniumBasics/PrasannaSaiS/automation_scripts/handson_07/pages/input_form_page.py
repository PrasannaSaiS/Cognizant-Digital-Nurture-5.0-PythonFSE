"""
Hands-On 7 - Task 2, Step 57
InputFormPage: encapsulates locators and actions for the Input Form
Submit demo page (name, email, phone, address fields).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[type='tel']")
    ADDRESS_INPUT = (By.NAME, "message")  # form uses "message" as the address field
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg, h2.success-msg")

    def fill_form(self, name: str, email: str, phone: str, address: str):
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)

    def submit_form(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self) -> str:
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
