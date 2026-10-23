from dotenv import load_dotenv
from udemy_purchase_scraper.utils import loadOwned, loadPurchases
from udemy_purchase_scraper.process import exportAllExcel

load_dotenv()
purchases = loadPurchases()
owned = loadOwned()
exportAllExcel(owned, purchases)