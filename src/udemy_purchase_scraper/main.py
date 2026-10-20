#region Imports
from udemy_purchase_scraper import browser
from dotenv import load_dotenv
from seleniumbase import SB, BaseCase, Driver
#endregion

#region Load Settings
load_dotenv()
#endregion

#region Get the SB object from the generator
manager = browser.startBrowser()
sb: BaseCase = manager.__enter__() # Replace this with a with statement later
#endregion

#region Start the processing
#sb.activate_cdp_mode("https://www.udemy.com/")
sb.open("https://www.udemy.com/")
#endregion

#region Get the cookies
from udemy_purchase_scraper.utils import checkForceNewCookies, saveCookies, loadCookies
import os
import time

cookies_path = os.environ.get("COOKIES_PATH", "cookies.json")
# print(cookies_path)
# import pathlib
# print(pathlib.Path.cwd())
saveCookies(sb=sb, f_path=cookies_path, force_cookies=checkForceNewCookies())
loadCookies(sb=sb, f_path=cookies_path)
time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
#endregion

#region Purchase Scraping
from udemy_purchase_scraper.purchase import scraper as prs

result = prs.getPurchasePages(sb=sb)
#endregion