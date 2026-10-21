#region Imports
from dotenv import load_dotenv
from udemy_purchase_scraper.utils import saveOwned, savePurchases
from udemy_purchase_scraper.login import checkLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
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
# with ThreadPoolExecutor(max_workers=2) as executor:
#     purchases = executor.submit(taskPurchases)
#     owned = executor.submit(taskOwned)
#     wait([purchases, owned])
#     purchases = purchases.result()
#     owned = owned.result()

from udemy_purchase_scraper.utils import uniqueCourses
import requests
from udemy_purchase_scraper.utils import requestsCookiesFromSelenium
from udemy_purchase_scraper.owned.scraper import getOwnedCurrentURLRequest

with ThreadPoolExecutor(max_workers=2) as executor:
    futures_map = {
        executor.submit(taskPurchases): "purchases",
        executor.submit(taskOwned): "owned"
    }
    for future in as_completed(futures_map):
        if futures_map[future] == "owned":
            owned = uniqueCourses(future.result())
            requests_cookies = requestsCookiesFromSelenium()
            with requests.Session() as session:
                session.cookies = requests_cookies
                for ind, course in enumerate(owned):
                    owned[ind].course_page = f"{getOwnedCurrentURLRequest(session=session, course_link=course.course_link)}/"
        else:
            purchases = future.result()
            
#endregion

# savePurchases(purchases)
# saveOwned(owned)