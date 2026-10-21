from udemy_purchase_scraper import browser
from udemy_purchase_scraper.purchase.scraper import getPurchasePages
from udemy_purchase_scraper.utils import loadCookies
import time
import os

def taskPurchases() -> None:
    """
    x
    """
    manager = browser.startBrowser()
    with manager as sb:
        sb.goto("https://www.udemy.com/")
        loadCookies(sb=sb)
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
        purchase_result = getPurchasePages(sb=sb)
        return(purchase_result)