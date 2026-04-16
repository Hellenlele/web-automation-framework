"""
Example: Login page test using Page Object Model.
Target: https://the-internet.herokuapp.com/login (free public test site)
"""
import pytest
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.config.config import Config


# ── Locators ──────────────────────────────────────────────────────────────────

USERNAME = (By.ID, "username")
PASSWORD = (By.ID, "password")
LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
FLASH_MSG = (By.CSS_SELECTOR, ".flash")
LOGOUT_BTN = (By.CSS_SELECTOR, "a[href='/logout']")


# ── Page Object ───────────────────────────────────────────────────────────────

class LoginPage(BasePage):
    def open_login(self):
        self.open(Config.LOGIN_URL)

    def login(self, username: str, password: str):
        self.type(USERNAME, username)
        self.type(PASSWORD, password)
        self.click(LOGIN_BTN)

    def get_flash_message(self) -> str:
        return self.get_text(FLASH_MSG)

    def logout(self):
        self.click(LOGOUT_BTN)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestLogin:
    def test_failed_login_wrong_username(self, class_driver):
        page = LoginPage(class_driver)
        page.open_login()
        page.login("wronguser", Config.LOGIN_PASSWORD)
        assert "Your username is invalid!" in page.get_flash_message()

    def test_failed_login_wrong_password(self, class_driver):
        page = LoginPage(class_driver)
        page.open_login()
        page.login(Config.LOGIN_USERNAME, "wrongpassword")
        assert "Your password is invalid!" in page.get_flash_message()

    def test_successful_login(self, class_driver):
        page = LoginPage(class_driver)
        page.open_login()
        page.login(Config.LOGIN_USERNAME, Config.LOGIN_PASSWORD)
        assert "You logged into a secure area!" in page.get_flash_message()

    def test_logout_after_login(self, class_driver):
        page = LoginPage(class_driver)
        page.open_login()
        page.login(Config.LOGIN_USERNAME, Config.LOGIN_PASSWORD)
        page.logout()
        assert "login" in page.current_url
