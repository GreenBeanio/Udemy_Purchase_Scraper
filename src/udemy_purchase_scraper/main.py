#region Imports
from udemy_purchase_scraper import browser
from dotenv import load_dotenv
from seleniumbase import BaseCase
from udemy_purchase_scraper.utils import checkForceNewCookies, saveCookies, loadCookies, checkHeadless, checkUseHeadless
from udemy_purchase_scraper.exceptions import BadCookies, RetryError, NeedHead
import time
import os
from pathlib import Path
#endregion

#region Load Settings
load_dotenv()
#endregion

def watchLogin(sb: BaseCase) -> None:
    """
    x
    """
    sb.maximize()
    sb.execute_script("alert('Login to Udemy to continue');")
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
    manager = browser.startBrowser()
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

checkLogin()

# #region Get the SB object from the generator
# manager = browser.startBrowser()
# sb: BaseCase = manager.__enter__() # Replace this with a with statement later
# #endregion

# #region Start the processing
# sb.goto("https://www.udemy.com/")
# #endregion

# #region Get the cookies
# from udemy_purchase_scraper.utils import checkForceNewCookies, saveCookies, loadCookies
# import os
# import time

# saveCookies(sb=sb, force_cookies=checkForceNewCookies())
# loadCookies(sb=sb)
# time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
# #endregion

# #region Purchase Scraping
# from udemy_purchase_scraper.purchase import scraper as prs
# purchase_result = prs.getPurchasePages(sb=sb)

# from udemy_purchase_scraper.owned import scraper as ors
# owned_result = ors.getOwnedPages(sb=sb)

# #endregion