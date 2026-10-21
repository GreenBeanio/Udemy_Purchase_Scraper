#region Imports
from dotenv import load_dotenv
from udemy_purchase_scraper.utils import saveOwned, savePurchases
from udemy_purchase_scraper.login import checkLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from concurrent.futures import ThreadPoolExecutor, wait
import sys
#endregion

# Make Selenium be multi-threaded
sys.argv.append("-n")

#region Load Settings
load_dotenv()
#endregion

#region Login
checkLogin()
#endregion

#region Scrape Data
with ThreadPoolExecutor(max_workers=2) as executor:
    purchases = executor.submit(taskPurchases)
    owned = executor.submit(taskOwned)
    wait([purchases, owned])
    purchases = purchases.result()
    owned = owned.result()
#endregion

savePurchases(purchases)
saveOwned(owned)