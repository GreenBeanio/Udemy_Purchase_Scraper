#region Imports
from dotenv import load_dotenv
from udemy_purchase_scraper.utils import saveOwned, savePurchases
from udemy_purchase_scraper.login import checkLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
import sys
#endregion

# Make Selenium be multi-threaded
sys.argv.append("-n")

#region Load Settings
load_dotenv()
#endregion

#region Scrape Data
purchases = taskPurchases()
owned = taskOwned()

savePurchases(purchases)
saveOwned(owned)