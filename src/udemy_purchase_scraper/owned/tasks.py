from udemy_purchase_scraper.config import CONFIG
from udemy_purchase_scraper import browser
from udemy_purchase_scraper.owned.scraper import getOwnedPages, getOwnedCurrentURLs
from udemy_purchase_scraper.utils import loadCookies
from udemy_purchase_scraper.owned.classes import UdemyCourseOwn
import time
import os
import logging

logger = logging.getLogger(__name__)

def taskOwned() -> list[UdemyCourseOwn]:
    """
    Multithreading task to scrape owned Udemy courses
    """
    manager = browser.startBrowser()
    with manager as sb:
        sb.goto("https://www.udemy.com/")
        loadCookies(sb=sb)
        time.sleep(CONFIG.SLEEP_TIME)
        owned_result = getOwnedPages(sb=sb)
        getOwnedCurrentURLs(owned_result)
        logging.info("Finished Scraping Owned")
        return owned_result 