from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from src.config.config import Config

_LINK = lambda text: (By.LINK_TEXT, text)


class HomePage(BasePage):
    def open(self):
        self.driver.get(Config.BASE_URL)

    def go_to(self, link_text: str):
        """Open the homepage, scroll to the named link, then click it."""
        self.open()
        self.scroll_to_element(_LINK(link_text))
        self.click(_LINK(link_text))
