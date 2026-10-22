#region Imports
from dotenv import load_dotenv
from udemy_purchase_scraper.utils import saveOwned, savePurchases
from udemy_purchase_scraper.login import checkLogin
from udemy_purchase_scraper.owned.tasks import taskOwned
from udemy_purchase_scraper.purchase.tasks import taskPurchases
from udemy_purchase_scraper.process import processItems
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, FIRST_COMPLETED
import sys
#endregion

def main():
    # Make Selenium be multi-threaded
    sys.argv.append("-n")
    load_dotenv()
    checkLogin()
    #region Scrape Data
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     purchases = executor.submit(taskPurchases)
    #     owned = executor.submit(taskOwned)
    #     wait([purchases, owned])
    #     purchases = purchases.result()
    #     owned = owned.result()
    #
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     futures_map = {
    #         executor.submit(taskPurchases): "purchases",
    #         executor.submit(taskOwned): "owned"
    #     }
    #     final_result = {}
    #     for future in as_completed(futures_map):
    #         if futures_map[future] == "owned":
    #             owned = uniqueCourses(future.result())
    #             final_result["owned"] = getOwnedCurrentURLs(owned)
    #         else:
    #             final_result["purchases"] = future.result()
    #
    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     futures_map = {
    #         executor.submit(taskPurchases): "purchases",
    #         executor.submit(taskOwned): "owned"
    #     }
    #     final_result = {}
    #     while futures_map:
    #         done, _ = wait(futures_map.keys(), return_when=FIRST_COMPLETED)
    #         for future in done:
    #             current_future = futures_map.pop(future)
    #             # Should be simple enough logic to not need a state machine or registry type pattern
    #             if current_future == "owned":
    #                 unique_future = executor.submit(uniqueCourses, future.result())
    #                 futures_map[unique_future] = "unique"
    #             elif current_future == "unique":
    #                 url_future = executor.submit(getOwnedCurrentURLs, future.result())
    #                 futures_map[url_future] = "url"
    #             elif current_future == "url":
    #                 final_result["owned"] = future.result()
    #             else:
    #                 final_result["purchases"] = future.result()
    #
    # savePurchases(final_result["purchases"])
    # saveOwned(final_result["owned"])
    with ThreadPoolExecutor(max_workers=2) as executor:
        purchases = executor.submit(taskPurchases)
        owned = executor.submit(taskOwned)
        wait([purchases, owned])
        purchases = purchases.result()
        owned = owned.result()
    processItems(owned, purchases)
    savePurchases(purchases)
    saveOwned(owned)

if __name__ == "__main__":
    main()