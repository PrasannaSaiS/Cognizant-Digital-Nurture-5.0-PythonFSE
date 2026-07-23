"""
Hands-On 5 - Task 2: WebDriverWait and Expected Conditions
"""

import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "hands_on_4"))
from setup_test import build_driver  # noqa: E402

from selenium.webdriver.common.by import By  # noqa: E402
from selenium.webdriver.support.ui import WebDriverWait  # noqa: E402
from selenium.webdriver.support import expected_conditions as EC  # noqa: E402
from selenium.common.exceptions import NoSuchElementException  # noqa: E402
from selenium.webdriver.support.ui import WebDriverWait as FluentWait  # noqa: E402

ALERTS_URL = "https://www.lambdatest.com/selenium-playground/bootstrap-alerts"


def test_explicit_wait_for_success_alert():
    """Step 36: click button, wait for alert to become visible, assert text."""
    driver = build_driver(headless=True)
    try:
        driver.get(ALERTS_URL)

        success_button = driver.find_element(By.ID, "success-alert")
        success_button.click()

        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert.text.lower()
        print("Success alert text:", alert.text)
    finally:
        driver.quit()


def test_sleep_vs_explicit_wait_timing_comparison():
    """
    Step 37: compare a hard sleep vs an explicit wait.

    time.sleep(3) is bad because it ALWAYS waits the full 3 seconds, even
    if the element appeared after 200ms (wasting time on fast machines/
    fast networks), and it FAILS unpredictably if the element takes longer
    than 3 seconds to appear on a slow machine/network. An explicit wait polls repeatedly up to a maximum timeout and
    returns AS SOON AS the condition is met - faster on fast machines,
    and more reliable on slow ones.
    """
    driver = build_driver(headless=True)
    try:
        # --- Version A: hard sleep ---
        driver.get(ALERTS_URL)
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        time.sleep(3)
        alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        assert alert.is_displayed()
        sleep_duration = time.time() - start
        print(f"time.sleep(3) version took: {sleep_duration:.2f}s")

        # --- Version B: explicit wait ---
        driver.get(ALERTS_URL)
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert alert.is_displayed()
        wait_duration = time.time() - start
        print(f"Explicit wait version took: {wait_duration:.2f}s")

        # On a fast local page like this, the explicit wait version should  typically be faster (or at worst equal) since it doesn't force a fixed 3-second delay.
    finally:
        driver.quit()


def test_element_to_be_clickable():
    """
    Step 38: wait for an element to be clickable before clicking it.

    visibility_of_element_located: only confirms the element is present in
    the DOM and has non-zero size (visible), but it might still be
    disabled or covered by another element (e.g., a loading overlay).

    element_to_be_clickable: confirms the element is visible AND enabled
    AND not obscured by anything else on top of it , a real click
    would actually succeed. Always prefer this immediately before a
    .click() call.
    """
    driver = build_driver(headless=True)
    try:
        driver.get(ALERTS_URL)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "success-alert"))
        )
        button.click()
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert alert.is_displayed()
    finally:
        driver.quit()


def test_fluent_wait_for_dynamic_table_row():
    """Step 39: FluentWait."""
    driver = build_driver(headless=True)
    try:
        driver.get(
            "https://www.lambdatest.com/selenium-playground/table-sort-search-filter-pagination"
        )

        wait = FluentWait(driver, timeout=10, poll_frequency=0.5).ignore(
            NoSuchElementException
        )

        first_row = wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr")
        )
        assert first_row.is_displayed()
        print("Dynamically-loaded table row located via FluentWait.")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_explicit_wait_for_success_alert()
    test_sleep_vs_explicit_wait_timing_comparison()
    test_element_to_be_clickable()
    test_fluent_wait_for_dynamic_table_row()
