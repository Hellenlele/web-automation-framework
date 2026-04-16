from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from src.config.config import Config


class BrowserHelper:
    """Manages browser driver creation and configuration.
    Uses Selenium's built-in driver manager (Selenium 4.6+) — no webdriver-manager needed.
    """

    @staticmethod
    def get_driver() -> webdriver.Remote:
        browser = Config.BROWSER.lower()
        if browser == "chrome":
            return BrowserHelper._get_chrome_driver()
        elif browser == "firefox":
            return BrowserHelper._get_firefox_driver()
        elif browser == "edge":
            return BrowserHelper._get_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}. Choose chrome, firefox, or edge.")

    @staticmethod
    def _get_chrome_driver() -> webdriver.Chrome:
        options = ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=options)

    @staticmethod
    def _get_firefox_driver() -> webdriver.Firefox:
        options = FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        return webdriver.Firefox(options=options)

    @staticmethod
    def _get_edge_driver() -> webdriver.Edge:
        options = EdgeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Edge(options=options)


"""
options.add_argument()
In short — it's how you configure the browser's startup behavior before Selenium hands control to your tests.
    --headless=new          │ Run without a visible window                           │
  ├─────────────────────────┼────────────────────────────────────────────────────────┤
  │ --no-sandbox            │ Required in Linux/CI environments (Docker)             │
  ├─────────────────────────┼────────────────────────────────────────────────────────┤                                                                                               
  │ --disable-dev-shm-usage │ Prevents crashes in Docker (limited shared memory)     │
  ├─────────────────────────┼────────────────────────────────────────────────────────┤                                                                                               
  │ --disable-gpu           │ Avoids GPU rendering issues in headless mode           │
  ├─────────────────────────┼────────────────────────────────────────────────────────┤                                                                                               
  │ --window-size=1920,1080 │ Sets a consistent viewport size for screenshots/layout │
  ├─────────────────────────┼────────────────────────────────────────────────────────┤                                                                                               
  │ --disable-notifications │ Blocks browser notification popups                   

"""