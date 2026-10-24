#region Imports
from dotenv import load_dotenv
from udemy_purchase_scraper.login import handleLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from udemy_purchase_scraper.process import processItems, exportAllExcel
from concurrent.futures import ThreadPoolExecutor, wait
import sys
from pathlib import Path
import os
import logging
#endregion

def main():
    """
    The main function to scrape your Udemy purchases and owned courses
    """
    # Make Selenium be multi-threaded
    sys.argv.append("-n")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s",
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler(Path(os.environ.get("LOG_PATH", "udemy.log")))
                        ])
    load_dotenv()
    handleLogin()
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="Scraper") as executor:
        purchases = executor.submit(taskPurchases)
        owned = executor.submit(taskOwned)
        wait([purchases, owned])
        purchases = purchases.result()
        owned = owned.result()
    processItems(owned, purchases)
    exportAllExcel(owned, purchases)

if __name__ == "__main__":
    main()