"""
Hands-On 6 - Task 1 - conftest.py
Step 41: function-scoped driver fixture.

scope='function' -> a fresh browser instance per test, so every test is
fully isolated (no shared cookies / open tabs / leftover state).
scope='session' would reuse a single browser across all tests - faster,
but risks one test's state leaking into and breaking the next.

The yield splits this fixture into setup (before yield) and teardown
(after yield) - equivalent to setUp/tearDown in unittest.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)

    yield drv  #  test runs here

    drv.quit()  # teardown after yield 
