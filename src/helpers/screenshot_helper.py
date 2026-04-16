import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from src.config.config import Config


class ScreenshotHelper:
    """Handles screenshot capture for full page and individual elements."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)

    def _build_path(self, name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        return os.path.join(Config.SCREENSHOT_DIR, filename)

    def take(self, name: str = "screenshot") -> str:
        """Capture the full browser viewport."""
        path = self._build_path(name)
        self.driver.save_screenshot(path)
        print(f"Screenshot saved: {path}")
        return path

    def take_element(self, element: WebElement, name: str = "element") -> str:
        """Capture a specific element."""
        path = self._build_path(name)
        element.screenshot(path)
        print(f"Element screenshot saved: {path}")
        return path

    def take_on_failure(self, test_name: str) -> str:
        """Capture screenshot on test failure."""
        if Config.SCREENSHOT_ON_FAIL:
            return self.take(f"FAIL_{test_name}")
        return ""
