"""
Example: Form interactions — inputs, checkboxes, dropdowns, file upload.
Target: https://the-internet.herokuapp.com (free public test site)
"""
import pytest
import os
from selenium.webdriver.common.by import By
from src.components.form import FormComponent
from src.components.dropdown import DropdownComponent
from src.pages.home_page import HomePage


# ── Checkbox Tests ────────────────────────────────────────────────────────────

CHECKBOX_1 = (By.CSS_SELECTOR, "form#checkboxes input:nth-of-type(1)")
CHECKBOX_2 = (By.CSS_SELECTOR, "form#checkboxes input:nth-of-type(2)")

class TestCheckboxes:
    def test_check_first_checkbox(self, driver):
        page = FormComponent(driver)
        HomePage(driver).go_to("Checkboxes")
        page.tick_checkbox(CHECKBOX_1, should_check=True)
        assert page.is_checked(CHECKBOX_1)

    def test_uncheck_second_checkbox(self, driver):
        page = FormComponent(driver)
        HomePage(driver).go_to("Checkboxes")
        page.tick_checkbox(CHECKBOX_2, should_check=False)
        assert not page.is_checked(CHECKBOX_2)


# ── Dropdown Tests ────────────────────────────────────────────────────────────

NATIVE_DROPDOWN = (By.ID, "dropdown")

class TestDropdown:
    def test_select_option_by_text(self, driver):
        page = DropdownComponent(driver)
        HomePage(driver).go_to("Dropdown")
        page.native_select_by_text(NATIVE_DROPDOWN, "Option 1")
        assert page.native_get_selected(NATIVE_DROPDOWN) == "Option 1"

    def test_select_option_by_value(self, driver):
        page = DropdownComponent(driver)
        HomePage(driver).go_to("Dropdown")
        page.native_select_by_value(NATIVE_DROPDOWN, "2")
        assert page.native_get_selected(NATIVE_DROPDOWN) == "Option 2"

    def test_all_options_listed(self, driver):
        page = DropdownComponent(driver)
        HomePage(driver).go_to("Dropdown")
        options = page.native_get_all_options(NATIVE_DROPDOWN)
        assert "Option 1" in options
        assert "Option 2" in options


# ── File Upload Tests ─────────────────────────────────────────────────────────

FILE_INPUT = (By.ID, "file-upload")
UPLOAD_BTN = (By.ID, "file-submit")
UPLOAD_RESULT = (By.ID, "uploaded-files")

class TestFileUpload:
    def test_upload_file(self, driver, tmp_path):
        # Create a temporary file to upload
        test_file = tmp_path / "test_upload.txt"
        test_file.write_text("hello automation")

        page = FormComponent(driver)
        HomePage(driver).go_to("File Upload")
        page.upload_file(FILE_INPUT, str(test_file))
        page.submit_form(button_locator=UPLOAD_BTN)
        assert page.get_text(UPLOAD_RESULT) == "test_upload.txt"
