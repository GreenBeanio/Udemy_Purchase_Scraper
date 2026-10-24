from udemy_purchase_scraper.config import CONFIG
from udemy_purchase_scraper.login import handleLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from udemy_purchase_scraper.process import processItems, exportAllExcel
from udemy_purchase_scraper.utils import checkLogLevel
from concurrent.futures import ThreadPoolExecutor, wait
import sys
import logging
import argparse
from pathlib import Path

def main():
    """
    The main function to scrape your Udemy purchases and owned courses
    """
    parser = argparse.ArgumentParser(
        description="Scrapes Udemy for your purchases.")
    parser.add_argument("-e", "--env",
                        type = str,
                        help="Path to the target .env file")
    parser.add_argument("-ll", "--log-level",
                        type = str,
                        help="Logging Level: DEBUG, INFO, WARNING, ERROR, CRITICAL. (Default: INFO)",
                        default="INFO")
    parser.add_argument("-lf", "--log-file",
                        type = str,
                        help="Path for the log file (Default: Udemy.log)",
                        default="Udemy.log")
    args = parser.parse_args()
    logging.basicConfig(level=checkLogLevel(args.log_level),
                            format="%(asctime)s [%(threadName)s] %(levelname)s: %(message)s",
                            handlers=[
                                logging.StreamHandler(),
                                logging.FileHandler(Path(args.log_file))
                            ])
    CONFIG.load(args.env)
    sys.argv.append("-n") # Make Selenium be multi-threaded
    driver_list = []
    try:
        handleLogin(driver_list=driver_list)
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="Scraper") as executor:
            purchases = executor.submit(taskPurchases, driver_list=driver_list)
            owned = executor.submit(taskOwned, driver_list=driver_list)
            wait([purchases, owned])
            purchases = purchases.result()
            owned = owned.result()
        processItems(owned, purchases)
        exportAllExcel(owned, purchases)
    except KeyboardInterrupt:
        logging.critical("Cancelled form Keyboard Interrupt")
    finally:
        for driver in driver_list:
            try:
                driver.quit()
                logging.info("Selenium driver closed")
            except:
                logging.critical("Selenium driver failed to quit")

if __name__ == "__main__":
    main()