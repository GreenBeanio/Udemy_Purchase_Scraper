from udemy_purchase_scraper.config import CONFIG
import os
from seleniumbase import BaseCase
import time
from udemy_purchase_scraper.exceptions import BadCookies
from udemy_purchase_scraper.browser import startBrowser
from udemy_purchase_scraper.utils import checkUseHeadless, saveCookies, loadCookies
from udemy_purchase_scraper.exceptions import NeedHead, RetryError
import logging

logger = logging.getLogger(__name__)

def checkLogin(sb: BaseCase) -> None:
    """
    Checks Selenium for the Udemy login status
    """
    sb.maximize()
    sb.set_messenger_theme(theme="flat", location="top_center")
    sb.post_message("Login to Udemy to continue")
    while True:
        login_button = sb.is_element_present("a[data-purpose='header-login']")
        if login_button:
            time.sleep(5)
        else:
            break
    saveCookies(sb=sb)
             
def attemptLogin(is_headless: bool, driver_list: list = None) -> None:
    """
    Attempts logging into Udemy
    """
    manager = startBrowser(is_headless=is_headless, driver_list=driver_list)
    with manager as sb:
        sb.minimize()
        sb.goto("https://www.udemy.com/")
        sb.minimize()
        time.sleep(CONFIG.SLEEP_TIME)
        if CONFIG.FORCE_NEW_COOKIES:
            if CONFIG.HEADLESS:
                raise NeedHead("In headless mode but need headed for login")
            checkLogin(sb=sb)
        else:
            try:
                loadCookies(sb=sb)
            except:
                if is_headless:
                    raise NeedHead("In headless mode but need headed for login")
                checkLogin(sb=sb)
        sb.refresh()
        time.sleep(CONFIG.SLEEP_TIME)
        login_button = sb.is_element_present("a[data-purpose='header-login']")
        if login_button:
            CONFIG.COOKIES_PATH.unlink()
            raise BadCookies("Login was unsuccessful")

def handleLogin(driver_list: list = None) -> None:
    """
    Handles logging into Udemy
    """
    cur_headless = checkUseHeadless()
    retry = 0
    logger.info("Attempting to login")
    while retry < int(CONFIG.SLEEP_TIME):
        try:
            attemptLogin(cur_headless)
            logger.info("Logged in successfully")
            return None
        except NeedHead:
            # Don't count this as a failed attempt since they didn't get a chance to log in
            cur_headless = False
            logger.info("Activating Headed mode for manual login")
        except:
            retry = retry + 1
            logger.warning("Unsuccessful login")
    logger.critical("Ran out of login attempts")
    raise RetryError("Ran out of retries")