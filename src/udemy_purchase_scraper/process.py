from udemy_purchase_scraper.owned.classes import UdemyCoursePurchaseDetails
from udemy_purchase_scraper.protocols import ExcelOutputable
import pandas as pd
import os
from pathlib import Path
from typing import Literal
import logging

logger = logging.getLogger(__name__)

def getOwnedDict(owned: any):
    """
    x
    Needs owned in oldest to newest such as from getOwnedPages
    """
    owned_dict = {}
    for course in owned:
        owned_dict[course.course_page] = course
    return owned_dict 

def recalculatePurchases(purchases, owned_dict):
    """
    x
    Needs purchases in oldest to newest such as from getPurchasePages
    """
    purchases.reverse() # Logic needs to be in newest to oldest
    purchase_dict = {}
    for ind, purchase in enumerate(purchases):
        original_lengths = len(purchase.courses)
        purchase.courses = [course for course in purchase.courses if course.course_link in owned_dict and course.course_link not in purchase_dict]
        for course in purchase.courses:
            purchase_dict[course.course_link] = None
        if len(purchase.courses) != original_lengths:
            purchases[ind].purchase_cost = sum([course.course_cost for course in purchase.courses])
    purchases = [purchase for purchase in purchases if len(purchase.courses) != 0]
    purchases.reverse() # Return it as oldest to newest to match the input
    return purchases 

def getCoursePurchaseDetails(purchases):
    """
    x
    """
    course_details = {}
    for purchase in purchases:
        for course in purchase.courses:
            course_details[course.course_link] = UdemyCoursePurchaseDetails(
                course_purchase=purchase.purchase_number, 
                course_date=purchase.purchase_date, 
                course_cost=course.course_cost)
    return course_details 

def mergeOwned(owned, course_purchase_details):
    """
    x
    """
    for crs_ind, course in enumerate(owned):
        if course.course_page in course_purchase_details:
            owned[crs_ind].purchase = course_purchase_details[course.course_page]

def processItems(owned, purchases):
    """
    x
    """
    owned_dict = getOwnedDict(owned)
    purchases = recalculatePurchases(purchases, owned_dict)
    course_purchase_details = getCoursePurchaseDetails(purchases)
    mergeOwned(owned, course_purchase_details)
    logger.info("Items Processed")

def toDF(source_list: ExcelOutputable) -> pd.DataFrame:
    """
    x
    """
    return pd.DataFrame([item.toExcelDict() for item in source_list])

def exportAllExcel(owned, purchases):
    """
    x
    """
    output_path = Path(os.environ.get("OUTPUT_PATH", "Udemy.xlsx"))
    with pd.ExcelWrixter(output_path, engine="openpyxl") as writer:
        toDF(purchases).to_excel(writer,
                                 sheet_name="Purchase", 
                                 index=False)
        toDF(owned).to_excel(writer,
                             sheet_name="Course", 
                             index=False)
    logger.info("Exported to Excel")
        