import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://example.com")
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT: int = int(os.getenv("EXPLICIT_WAIT", "20"))
    SCREENSHOT_ON_FAIL: bool = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() == "true"
    SCREENSHOT_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "screenshots")
    LOGIN_USERNAME: str = os.getenv("LOGIN_USERNAME", "tomsmith")
    LOGIN_PASSWORD: str = os.getenv("LOGIN_PASSWORD", "SuperSecretPassword!")
    LOGIN_URL: str = os.getenv("LOGIN_URL", "https://the-internet.herokuapp.com/login")
