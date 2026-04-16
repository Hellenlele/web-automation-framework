from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from src.config.config import Config
from src.helpers.wait_helper import WaitHelper
from src.helpers.screenshot_helper import ScreenshotHelper


class BasePage:
    """
    Base class for all Page Objects.
    Wraps common Selenium interactions with built-in waits.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.screenshot = ScreenshotHelper(driver)
        self.actions = ActionChains(driver)
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)

    # ── Navigation ────────────────────────────────────────────────────────────

    def open(self, url: str):
        self.driver.get(url)

    def open_base(self, path: str = ""):
        self.driver.get(Config.BASE_URL + path)

    def refresh(self):
        self.driver.refresh()

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def title(self) -> str:
        return self.driver.title

    # ── Finding Elements ───────────────────────────────────────────────────────

    def find(self, locator: tuple) -> WebElement:
        return self.wait.until_visible(locator)

    def find_all(self, locator: tuple) -> list[WebElement]:
        return self.wait.until_all_visible(locator)

    def find_present(self, locator: tuple) -> WebElement:
        """Find element in DOM even if not visible."""
        return self.wait.until_present(locator)

    # ── Interactions ───────────────────────────────────────────────────────────

    def click(self, locator: tuple):
        self.wait.until_clickable(locator).click()

    def double_click(self, locator: tuple):
        element = self.find(locator)
        self.actions.double_click(element).perform()

    def right_click(self, locator: tuple):
        element = self.find(locator)
        self.actions.context_click(element).perform()

    def type(self, locator: tuple, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def clear(self, locator: tuple):
        self.find(locator).clear()

    def press_key(self, locator: tuple, key: str):
        self.find(locator).send_keys(key)

    def submit(self, locator: tuple):
        self.find(locator).submit()

    # ── Mouse Actions ──────────────────────────────────────────────────────────

    def hover(self, locator: tuple):
        element = self.find(locator)
        self.actions.move_to_element(element).perform()

    def drag_and_drop(self, source_locator: tuple, target_locator: tuple):
        source = self.find(source_locator)
        target = self.find(target_locator)
        self.actions.drag_and_drop(source, target).perform()

    def drag_and_drop_by_offset(self, locator: tuple, x_offset: int, y_offset: int):
        element = self.find(locator)
        self.actions.drag_and_drop_by_offset(element, x_offset, y_offset).perform()

    def click_and_hold(self, locator: tuple):
        element = self.find(locator)
        self.actions.click_and_hold(element).perform()

    def release(self):
        self.actions.release().perform()

    # ── Reading Values ─────────────────────────────────────────────────────────

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        return self.find(locator).get_attribute(attribute)

    def get_value(self, locator: tuple) -> str:
        return self.get_attribute(locator, "value")

    def is_displayed(self, locator: tuple) -> bool:
        return self.wait.is_visible(locator)

    def is_enabled(self, locator: tuple) -> bool:
        return self.find(locator).is_enabled()

    def is_checked(self, locator: tuple) -> bool:
        return self.find(locator).is_selected()

    # ── Dropdowns ──────────────────────────────────────────────────────────────

    def select_by_text(self, locator: tuple, text: str):
        Select(self.find(locator)).select_by_visible_text(text)

    def select_by_value(self, locator: tuple, value: str):
        Select(self.find(locator)).select_by_value(value)

    def select_by_index(self, locator: tuple, index: int):
        Select(self.find(locator)).select_by_index(index)

    def get_selected_option(self, locator: tuple) -> str:
        return Select(self.find(locator)).first_selected_option.text

    def get_all_options(self, locator: tuple) -> list[str]:
        return [opt.text for opt in Select(self.find(locator)).options]

    # ── Checkbox & Radio ───────────────────────────────────────────────────────

    def check(self, locator: tuple):
        if not self.is_checked(locator):
            self.click(locator)

    def uncheck(self, locator: tuple):
        if self.is_checked(locator):
            self.click(locator)

    # ── Scrolling ─────────────────────────────────────────────────────────────

    def scroll_to_element(self, locator: tuple):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_by(self, x: int, y: int):
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    # ── Alerts & Popups ───────────────────────────────────────────────────────

    def accept_alert(self) -> str:
        alert = self.wait.until_alert_present()
        text = alert.text
        alert.accept()
        return text

    def dismiss_alert(self) -> str:
        alert = self.wait.until_alert_present()
        text = alert.text
        alert.dismiss()
        return text

    def type_in_alert(self, text: str):
        alert = self.wait.until_alert_present()
        alert.send_keys(text)
        alert.accept()

    # ── iFrames ───────────────────────────────────────────────────────────────

    def switch_to_frame(self, locator: tuple):
        frame = self.find_present(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_frame_by_index(self, index: int):
        self.driver.switch_to.frame(index)

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    # ── Windows & Tabs ────────────────────────────────────────────────────────

    def get_window_handles(self) -> list[str]:
        return self.driver.window_handles

    def switch_to_new_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def switch_to_window(self, handle: str):
        self.driver.switch_to.window(handle)

    def close_current_window(self):
        self.driver.close()

    def open_new_tab(self, url: str):
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.switch_to_new_window()

    # ── JavaScript ────────────────────────────────────────────────────────────

    def execute_js(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def click_via_js(self, locator: tuple):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def highlight(self, locator: tuple, color: str = "yellow"):
        element = self.find(locator)
        self.driver.execute_script(
            f"arguments[0].style.backgroundColor = '{color}';", element
        )

    # ── Cookies ───────────────────────────────────────────────────────────────

    def add_cookie(self, name: str, value: str):
        self.driver.add_cookie({"name": name, "value": value})

    def get_cookie(self, name: str) -> dict:
        return self.driver.get_cookie(name)

    def delete_cookie(self, name: str):
        self.driver.delete_cookie(name)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    # ── Wait Shortcuts ────────────────────────────────────────────────────────

    def wait_for_url(self, url_fragment: str):
        self.wait.until_url_contains(url_fragment)

    def wait_for_text(self, locator: tuple, text: str):
        self.wait.until_text_present(locator, text)

    def wait_until_hidden(self, locator: tuple):
        self.wait.until_invisible(locator)
