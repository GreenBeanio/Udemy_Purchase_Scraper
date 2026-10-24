from udemy_purchase_scraper.config import CONFIG
from udemy_purchase_scraper import browser
from udemy_purchase_scraper.purchase.scraper import getPurchasePages
from udemy_purchase_scraper.utils import loadCookies
from udemy_purchase_scraper.purchase.classes import UdemyPurchase
import time
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
        time.sleep(CONFIG.SLEEP_TIME)
        purchase_result = getPurchasePages(sb=sb)
        logging.info("Finished Scraping Purchases")
        return purchase_result 