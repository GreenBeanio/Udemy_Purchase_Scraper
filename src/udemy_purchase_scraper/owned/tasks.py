from udemy_purchase_scraper import browser
from udemy_purchase_scraper.owned.scraper import getOwnedPages
from udemy_purchase_scraper.utils import loadCookies
import time
import os

def taskOwned() -> None:
    """
    x
    """
    manager = browser.startBrowser()
    with manager as sb:
        sb.goto("https://www.udemy.com/")
        loadCookies(sb=sb)
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
        owned_result = getOwnedPages(sb=sb)
        return(owned_result)