from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from src.config.config import Config


class WaitHelper:
    """Custom wait strategies wrapping Selenium's WebDriverWait."""

    def __init__(self, driver: WebDriver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or Config.EXPLICIT_WAIT

    def until_visible(self, locator: tuple) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def until_clickable(self, locator: tuple) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def until_present(self, locator: tuple) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def until_invisible(self, locator: tuple) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def until_text_present(self, locator: tuple, text: str) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def until_url_contains(self, url_fragment: str) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(url_fragment)
        )

    def until_title_contains(self, title: str) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.title_contains(title)
        )

    def until_all_visible(self, locator: tuple) -> list[WebElement]:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def until_alert_present(self):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.alert_is_present()
        )

    def until_new_window_opened(self, current_handles: list) -> bool:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.new_window_is_opened(current_handles)
        )

    def is_visible(self, locator: tuple, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
