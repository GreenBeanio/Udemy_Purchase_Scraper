import os
from seleniumbase import BaseCase
import time
from udemy_purchase_scraper.exceptions import BadCookies
from udemy_purchase_scraper.browser import startBrowser
from udemy_purchase_scraper.utils import checkForceNewCookies, checkUseHeadless, checkHeadless, saveCookies, loadCookies
from udemy_purchase_scraper.exceptions import NeedHead, RetryError
from pathlib import Path

def watchLogin(sb: BaseCase) -> None:
    """
    x
    """
    sb.maximize()
    # sb.execute_script("alert('Login to Udemy to continue');")
    # sb.evaluate("alert('Login to Udemy to continue');")
    sb.set_messenger_theme(theme="flat", location="top_center")
    sb.post_message("Login to Udemy to continue")
    while True:
        login_button = sb.is_element_present("a[data-purpose='header-login']")
        if login_button:
            time.sleep(5)
        else:
            break
    saveCookies(sb=sb)
             
def attemptLogin() -> None:
    """
    x
    """
    manager = startBrowser()
    with manager as sb:
        sb.minimize()
        sb.goto("https://www.udemy.com/")
        sb.minimize()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
        if checkForceNewCookies():
            if checkUseHeadless():
                raise NeedHead("In headless mode but need headed for login")
            watchLogin(sb=sb)
        else:
            try:
                loadCookies(sb=sb)
            except :
                if checkUseHeadless():
                    raise NeedHead("In headless mode but need headed for login")
                watchLogin(sb=sb)

        sb.refresh()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))

        login_button = sb.is_element_present("a[data-purpose='header-login']")

        if login_button:
            cookies_path = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
            cookies_path.unlink()
            raise BadCookies("Login was unsuccessful")

def checkLogin() -> None:
    """
    x
    """
    original_headless = checkHeadless()
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            attemptLogin()
            os.environ["HEADLESS"] = "true" if original_headless else "false"
            return None
        except NeedHead:
            # Don't count this as a failed attempt since they didn't get a chance to log in
            os.environ["HEADLESS"] = "false"
        except:
            retry = retry + 1
    os.environ["HEADLESS"] = "true" if original_headless else "false"
    raise RetryError("Ran out of retries")