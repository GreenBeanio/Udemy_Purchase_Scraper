from udemy_purchase_scraper import browser
from udemy_purchase_scraper.purchase.scraper import getPurchasePages
from udemy_purchase_scraper.utils import loadCookies
from udemy_purchase_scraper.purchase.classes import UdemyPurchase
import time
import os
import logging

logger = logging.getLogger(__name__)

def taskPurchases() -> list[UdemyPurchase]:
    """
    Multithreading task to scrape Udemy purchases
    """
    manager = browser.startBrowser()
    with manager as sb:
        sb.goto("https://www.udemy.com/")
        loadCookies(sb=sb)
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
        purchase_result = getPurchasePages(sb=sb)
        logging.info("Finished Scraping Purchases")
        return purchase_result 