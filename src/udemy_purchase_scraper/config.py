from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)

def checkForceNewCookies() -> bool:
    """
    Checks for the FORCE_NEW_COOKIES environment variable
    """
    force_new_cookies = os.environ.get("FORCE_NEW_COOKIES", False)
    if isinstance(force_new_cookies, str):
        if force_new_cookies.lower() == "false":
            force_new_cookies = False
        elif force_new_cookies.lower() == "true":
            force_new_cookies = True
        else:
            force_new_cookies = False
    return force_new_cookies 

def checkChromeVersion() -> int|None:
    """
    Checks for the CHROME_VERSION environment variable
    """
    chrome_version = os.environ.get("CHROME_VERSION", None)
    if isinstance(chrome_version, str):
        if chrome_version.lower() == "none":
            chrome_version = None
        else:
            try:
                chrome_version = int(chrome_version)
            except:
                chrome_version = None
    return chrome_version 

def checkHeadless() -> bool:
    """
    Checks for the HEADLESS environment variable
    """
    run_headless = os.environ.get("HEADLESS", False)
    if isinstance(run_headless, str):
        run_headless = run_headless.lower() == "true"
    return run_headless 

class Config():
    """
    Gets the configuration settings from the environment variables
    """

    def __init__(self):
        self.SLEEP_TIME: int = None
        self.RETRY_LIMIT: int = None
        self.FORCE_NEW_COOKIES: bool = None
        self.COOKIES_PATH: Path = None
        self.CHROME_VERSION = None
        self.HEADLESS: bool = None
        self.OUTPUT_PATH: Path = None

    def load(self, env_path: str|None = None):
        if env_path is None:
            #path = Path(os.getcwd()) / ".env"
            path = Path(find_dotenv(usecwd=True))
        else:
            path = Path(env_path)
        if path.exists() and not path.is_dir():
            load_dotenv(path)
            logger.info("Loaded .env file")
        else:
            logger.warning("No .env file found using defaults")
        self.SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 3))
        self.RETRY_LIMIT = int(os.environ.get("RETRY_LIMIT", 3))
        self.FORCE_NEW_COOKIES = checkForceNewCookies()
        self.COOKIES_PATH = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
        self.CHROME_VERSION = checkChromeVersion()
        self.HEADLESS= checkHeadless()
        self.OUTPUT_PATH = Path(os.environ.get("OUTPUT_PATH", "Udemy.xlsx"))
        
# Create the singleton CONFIG object
CONFIG = Config()