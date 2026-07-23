""""
Hands-On 4 - Task 1: Selenium Architecture and Environment Setup

Selenium Components

1. WebDriver
- Controls the browser through browser drivers.
- Sends commands from Python to Chrome.

2. Selenium Grid
- Executes tests on multiple browsers and machines simultaneously.
- Used for parallel execution.

3. Selenium IDE
- Browser extension for recording and replaying test cases.
- Useful for beginners and quick automation.

Implicit Wait:
driver.implicitly_wait(10)

Implicit wait applies globally to every element lookup.
Although simple, it is generally discouraged because every
lookup waits unnecessarily. Explici t waits are more precise
and improve execution speed.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def build_driver(headless: bool = False):
    """Create and return a configured Chrome WebDriver instance."""
    options = Options()

    # Step 27: run headless - no visible browser window, still fully functional
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    # webdriver-manager auto-downloads the ChromeDriver version that
    # matches the installed Chrome browser, so no manual driver management.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Step 26: implicit wait
    # An implicit wait tells the driver to poll the DOM for up to N seconds
    # whenever ANY find_element call doesn't immediately find a match.
    driver.implicitly_wait(10)

    return driver


def test_open_playground_and_print_title():
    """Step 25 & 27: open the playground, print title, close browser."""
    driver = build_driver(headless=True)
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/")
        print("Page title:", driver.title)
        assert "Selenium" in driver.title or "Playground" in driver.title
    finally:
        driver.quit()


if __name__ == "__main__":
    test_open_playground_and_print_title()
