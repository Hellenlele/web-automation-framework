from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class FormComponent(BasePage):
    """
    Helpers for interacting with HTML forms:
    text inputs, checkboxes, radio buttons, file uploads, and submission.
    """

    def fill_field(self, locator: tuple, value: str):
        """Clear and type into a text/email/password input."""
        self.type(locator, value)

    def fill_form(self, field_map: dict):
        """
        Fill multiple fields at once.
        field_map: { locator_tuple: value, ... }
        """
        for locator, value in field_map.items():
            self.fill_field(locator, value)

    def tick_checkbox(self, locator: tuple, should_check: bool = True):
        """Check or uncheck a checkbox based on desired state."""
        if should_check:
            self.check(locator)
        else:
            self.uncheck(locator)

    def select_radio(self, locator: tuple):
        """Select a radio button."""
        self.click(locator)

    def upload_file(self, locator: tuple, file_path: str):
        """Send a file path to a file input element."""
        element = self.find_present(locator)
        element.send_keys(file_path)

    def submit_form(self, button_locator: tuple = None, form_locator: tuple = None):
        """Submit via button click or form submit()."""
        if button_locator:
            self.click(button_locator)
        elif form_locator:
            self.submit(form_locator)

    def get_validation_message(self, locator: tuple) -> str:
        """Read the browser's native HTML5 validation message."""
        element = self.find(locator)
        return self.driver.execute_script(
            "return arguments[0].validationMessage;", element
        )

    def is_field_valid(self, locator: tuple) -> bool:
        element = self.find(locator)
        return self.driver.execute_script(
            "return arguments[0].validity.valid;", element
        )
