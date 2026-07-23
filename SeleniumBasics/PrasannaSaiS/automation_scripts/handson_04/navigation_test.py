"""
Hands-On 4 - Task 2: WebDriver Navigation and Window Commands
"""

from selenium.webdriver.common.by import By
from setup_test import build_driver

BASE_URL = "https://www.lambdatest.com/selenium-playground/"


def test_navigation_and_back():
    """Step 28: navigate to Simple Form Demo."""
    driver = build_driver(headless=True)
    try:
        driver.get(BASE_URL)

        link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        link.click()

        assert "simple-form-demo" in driver.current_url

        driver.back()
        assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
    finally:
        driver.quit()


def test_multiple_windows_and_screenshot():
    """Steps 29-30: open a new tab, switch between tabs, take a screenshot."""
    driver = build_driver(headless=True)
    try:
        driver.get(BASE_URL)

        # Step 29: open a new tab via JS and switch to it
        driver.execute_script('window.open("https://www.google.com");')
        all_tabs = driver.window_handles
        assert len(all_tabs) == 2

        driver.switch_to.window(all_tabs[1])
        print("Second tab title:", driver.title)
        assert "Google" in driver.title

        # Step 30: switch back to the original tab and screenshot it
        driver.switch_to.window(all_tabs[0])
        screenshot_saved = driver.save_screenshot("playground_screenshot.png")
        assert screenshot_saved is True
    finally:
        driver.quit()


def test_window_size():
    """
    Step 31: get_window_size() / set_window_size().
    """
    driver = build_driver(headless=True)
    try:
        driver.get(BASE_URL)
        original_size = driver.get_window_size()
        print("Original window size:", original_size)

        driver.set_window_size(1280, 800)
        new_size = driver.get_window_size()
        assert new_size["width"] == 1280
        assert new_size["height"] == 800
    finally:
        driver.quit()


if __name__ == "__main__":
    test_navigation_and_back()
    test_multiple_windows_and_screenshot()
    test_window_size()
    print("All Hands-On 4 Task 2 checks passed.")
