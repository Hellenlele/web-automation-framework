import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from src.helpers.browser_helper import BrowserHelper
from src.helpers.screenshot_helper import ScreenshotHelper


@pytest.fixture(scope="session")
def driver() -> WebDriver:
    """Session-scoped driver: one browser for the entire test session."""
    _driver = BrowserHelper.get_driver()
    yield _driver
    _driver.quit()


@pytest.fixture(scope="class")
def class_driver() -> WebDriver:
    """Class-scoped driver: one browser shared across all tests in a class."""
    _driver = BrowserHelper.get_driver()
    yield _driver
    _driver.quit()


@pytest.fixture(scope="function")
def fresh_driver() -> WebDriver:
    """Function-scoped driver: a new browser for each test."""
    _driver = BrowserHelper.get_driver()
    yield _driver
    _driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Auto-screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("class_driver") or item.funcargs.get("fresh_driver")
        if driver:
            try:
                helper = ScreenshotHelper(driver)
                helper.take_on_failure(item.name)
            except Exception:
                pass
