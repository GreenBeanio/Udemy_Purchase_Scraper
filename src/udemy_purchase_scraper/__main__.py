from udemy_purchase_scraper.config import CONFIG
from udemy_purchase_scraper.login import handleLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from udemy_purchase_scraper.process import processItems, exportAllExcel
from udemy_purchase_scraper.utils import checkLogLevel
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, wait
import threading
import sys
import logging
import argparse
import signal

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

    def makeDaemon(*args, **kwargs):
        """
        Makes a thread a daemon thread
        """
        thread = threading.Thread(*args, **kwargs)
        thread.daemon = True
        return thread

    executor = ThreadPoolExecutor(
        max_workers=2, 
        thread_name_prefix="Scraper")
    executor._thread_factory = makeDaemon

    def handleShutdown(signum, frame):
        """
        Shuts down in the event of a keyboard interrupt
        """
        logging.critical("Cancelled form Keyboard Interrupt")
        executor.shutdown(wait=False, cancel_futures=True)
        logging.info("Thread Pool closed")
        if driver_list:
            for driver in driver_list:
                try:
                    driver.quit()
                    logging.info("Selenium driver closed")
                except:
                    logging.critical("Selenium driver failed to quit")
        sys.exit(130)

    signal.signal(signal.SIGINT, handleShutdown)

    try:
        handleLogin(driver_list=driver_list)
        purchases = executor.submit(taskPurchases, driver_list=driver_list)
        owned = executor.submit(taskOwned, driver_list=driver_list)
        wait([purchases, owned])
        purchases = purchases.result()
        owned = owned.result()
        processItems(owned, purchases)
        exportAllExcel(owned, purchases)
    except:
        logging.critical("Exception in main")
    finally:
        executor.shutdown()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        logging.info("Shutting Down")
        
if __name__ == "__main__":
    main()