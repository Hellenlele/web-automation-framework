from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class ModalComponent(BasePage):
    """
    Helpers for interacting with modal dialogs / overlay panels.
    Provide locators that match your app's modal structure.
    """

    def is_open(self, modal_locator: tuple) -> bool:
        return self.is_displayed(modal_locator)

    def wait_until_open(self, modal_locator: tuple):
        self.find(modal_locator)

    def wait_until_closed(self, modal_locator: tuple):
        self.wait_until_hidden(modal_locator)

    def get_title(self, title_locator: tuple) -> str:
        return self.get_text(title_locator)

    def get_body_text(self, body_locator: tuple) -> str:
        return self.get_text(body_locator)

    def confirm(self, confirm_button_locator: tuple):
        """Click the confirm / OK / Yes button."""
        self.click(confirm_button_locator)

    def cancel(self, cancel_button_locator: tuple):
        """Click the cancel / close / No button."""
        self.click(cancel_button_locator)

    def close_by_x(self, close_button_locator: tuple):
        """Click the × close button."""
        self.click(close_button_locator)

    def close_by_escape(self):
        from selenium.webdriver.common.keys import Keys
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def close_by_backdrop(self, backdrop_locator: tuple):
        """Click outside the modal on the backdrop to dismiss it."""
        self.click(backdrop_locator)
