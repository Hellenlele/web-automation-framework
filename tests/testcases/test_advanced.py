"""
Example: Advanced interactions — tables, modals, alerts, iframes,
         drag & drop, multiple windows, and JavaScript actions.
Target: https://the-internet.herokuapp.com (free public test site)
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.pages.base_page import BasePage
from src.pages.home_page import HomePage
from src.config.config import Config
from src.components.table import TableComponent


# ── Table Tests ───────────────────────────────────────────────────────────────

TABLE = (By.CSS_SELECTOR, "table#table1")

class TestTable:
    def test_read_headers(self, driver):
        page = TableComponent(driver)
        HomePage(driver).go_to("Sortable Data Tables")
        headers = page.get_headers(TABLE)
        assert "Last Name" in headers
        assert "First Name" in headers
        assert "Email" in headers

    def test_row_count(self, driver):
        page = TableComponent(driver)
        HomePage(driver).go_to("Sortable Data Tables")
        assert page.get_row_count(TABLE) == 4

    def test_find_row_by_name(self, driver):
        page = TableComponent(driver)
        HomePage(driver).go_to("Sortable Data Tables")
        row = page.find_row_by_text(TABLE, "Smith")
        assert row != -1

    def test_read_specific_cell(self, driver):
        page = TableComponent(driver)
        HomePage(driver).go_to("Sortable Data Tables")
        # Row 1, Col 1 should be a last name
        cell = page.get_cell(TABLE, 1, 1)
        assert isinstance(cell, str) and len(cell) > 0


# ── Alert Tests ───────────────────────────────────────────────────────────────

ALERT_BTN = (By.XPATH, "//button[text()='Click for JS Alert']")
CONFIRM_BTN = (By.XPATH, "//button[text()='Click for JS Confirm']")
PROMPT_BTN = (By.XPATH, "//button[text()='Click for JS Prompt']")
RESULT = (By.ID, "result")

class TestAlerts:
    def test_accept_alert(self, driver):
        page = BasePage(driver)
        HomePage(driver).go_to("JavaScript Alerts")
        page.click(ALERT_BTN)
        page.accept_alert()
        assert "You successfully clicked an alert" in page.get_text(RESULT)

    def test_dismiss_confirm(self, driver):
        page = BasePage(driver)
        HomePage(driver).go_to("JavaScript Alerts")
        page.click(CONFIRM_BTN)
        page.dismiss_alert()
        assert "You clicked: Cancel" in page.get_text(RESULT)

    def test_type_in_prompt(self, driver):
        page = BasePage(driver)
        HomePage(driver).go_to("JavaScript Alerts")
        page.click(PROMPT_BTN)
        page.type_in_alert("Hello Automation")
        assert "You entered: Hello Automation" in page.get_text(RESULT)


# ── iFrame Tests ──────────────────────────────────────────────────────────────

IFRAME = (By.ID, "mce_0_ifr")
IFRAME_BODY = (By.ID, "tinymce")

class TestIframe:
    def test_type_inside_iframe(self, driver):
        page = BasePage(driver)
        driver.get(Config.BASE_URL + "/iframe")
        # Use TinyMCE's JS API — more reliable than interacting with the raw iframe body
        page.execute_js("tinyMCE.activeEditor.setContent('Automation inside iframe');")
        content = page.execute_js(
            "return tinyMCE.activeEditor.getContent({format: 'text'});"
        )
        assert "Automation inside iframe" in content


# ── Multiple Windows Tests ────────────────────────────────────────────────────

NEW_WINDOW_BTN = (By.LINK_TEXT, "Click Here")
WINDOW_TITLE = (By.CSS_SELECTOR, "h3")

class TestWindows:
    def test_switch_to_new_window(self, driver):
        page = BasePage(driver)
        HomePage(driver).go_to("Multiple Windows")
        original_handle = driver.current_window_handle
        page.click(NEW_WINDOW_BTN)
        page.switch_to_new_window()
        assert "New Window" in page.get_text(WINDOW_TITLE)
        page.close_current_window()
        page.switch_to_window(original_handle)


# ── Hover Tests ───────────────────────────────────────────────────────────────

HOVER_FIGURE = (By.CSS_SELECTOR, ".figure:nth-of-type(1)")
HOVER_CAPTION = (By.CSS_SELECTOR, ".figure:nth-of-type(1) .figcaption")

class TestHover:
    def test_hover_reveals_element(self, driver):
        page = BasePage(driver)
        HomePage(driver).go_to("Hovers")
        page.hover(HOVER_FIGURE)
        assert page.is_displayed(HOVER_CAPTION)


# ── Drag & Drop Tests ─────────────────────────────────────────────────────────

DRAG_SOURCE = (By.ID, "column-a")
DRAG_TARGET = (By.ID, "column-b")

class TestDragDrop:
    def test_drag_and_drop(self, driver):
        page = BasePage(driver)
        HomePage(driver).go_to("Drag and Drop")
        page.drag_and_drop(DRAG_SOURCE, DRAG_TARGET)
        # After drag, column-a header should now say "B"
        assert page.get_text(DRAG_SOURCE) == "B"


# ── Scroll Tests ──────────────────────────────────────────────────────────────

FOOTER = (By.CSS_SELECTOR, "div#page-footer")

class TestScroll:
    def test_scroll_to_bottom(self, driver):
        page = BasePage(driver)
        HomePage(driver).open()
        page.scroll_to_bottom()
        page.scroll_to_element(FOOTER)
        assert page.is_displayed(FOOTER)
