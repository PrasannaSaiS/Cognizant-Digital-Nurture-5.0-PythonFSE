"""
Hands-On 7 - Task 1, Step 54
DropdownPage: encapsulates locators and actions for the Select Dropdown
List Demo page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class DropdownPage(BasePage):
    DAY_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name: str):
        dropdown_element = self.wait_for_element(self.DAY_DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_visible_text(day_name)

    def get_selected_day(self) -> str:
        dropdown_element = self.driver.find_element(*self.DAY_DROPDOWN)
        return Select(dropdown_element).first_selected_option.text
