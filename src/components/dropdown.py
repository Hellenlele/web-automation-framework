from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class DropdownComponent(BasePage):
    """
    Handles both native <select> dropdowns and custom JS dropdowns
    (e.g. Bootstrap Select, Select2, Material UI).
    """

    # ── Native <select> ───────────────────────────────────────────────────────

    def native_select_by_text(self, locator: tuple, text: str):
        self.select_by_text(locator, text)

    def native_select_by_value(self, locator: tuple, value: str):
        self.select_by_value(locator, value)

    def native_select_by_index(self, locator: tuple, index: int):
        self.select_by_index(locator, index)

    def native_get_selected(self, locator: tuple) -> str:
        return self.get_selected_option(locator)

    def native_get_all_options(self, locator: tuple) -> list[str]:
        return self.get_all_options(locator)

    # ── Custom Dropdown (click-to-open pattern) ───────────────────────────────

    def custom_open(self, trigger_locator: tuple):
        """Click the dropdown trigger to open the options list."""
        self.click(trigger_locator)

    def custom_select_option(self, trigger_locator: tuple, option_locator: tuple):
        """Open the dropdown then click the desired option."""
        self.custom_open(trigger_locator)
        self.click(option_locator)

    def custom_select_by_text(
        self, trigger_locator: tuple, options_locator: tuple, text: str
    ):
        """
        Open the dropdown then match an option by its visible text.
        options_locator should match all <li> / option items.
        """
        self.custom_open(trigger_locator)
        options = self.find_all(options_locator)
        for option in options:
            if option.text.strip() == text:
                option.click()
                return
        raise ValueError(f"Option '{text}' not found in dropdown.")

    def custom_get_selected_text(self, selected_locator: tuple) -> str:
        """Read the currently displayed selection text."""
        return self.get_text(selected_locator)

    def custom_search_and_select(
        self,
        trigger_locator: tuple,
        search_input_locator: tuple,
        option_locator: tuple,
        search_term: str,
    ):
        """For searchable dropdowns (e.g. Select2): open, type, then pick."""
        self.custom_open(trigger_locator)
        self.type(search_input_locator, search_term)
        self.click(option_locator)
