from udemy_purchase_scraper.owned.classes import UdemyCoursePurchaseDetails, UdemyCourseOwn
from udemy_purchase_scraper.purchase.classes import UdemyPurchase
from udemy_purchase_scraper.protocols import ExcelOutputable
import pandas as pd
import os
from pathlib import Path
from typing import Literal
import logging

logger = logging.getLogger(__name__)

def getOwnedDict(owned: list[UdemyCourseOwn]) -> dict[str, None]:
    """
    Gets dictionary of the newest instance owned course
    """
    owned_dict = {}
    for course in owned:
        owned_dict[course.course_page] = None
    return owned_dict 

def processPurchases(purchases: list[UdemyPurchase], owned_dict: dict):
    """
    Processes the purchases

    Filters the purchases to only include the newest purchase of a specific course and
    only courses that are actually owned and haven't been refunded.

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
    ind = 0
    while ind < len(purchases):
        if len(purchases[ind].courses) == 0:
            del purchases[ind]
        else:
            ind = ind + 1
    purchases.reverse() # Return it as oldest to newest to match the input

def getCoursePurchaseDetails(purchases: list[UdemyPurchase]) -> dict[str, UdemyCoursePurchaseDetails]:
    """
    Gets purchase details to add into the Udemy owned courses
    """
    course_details = {}
    for purchase in purchases:
        for course in purchase.courses:
            course_details[course.course_link] = UdemyCoursePurchaseDetails(
                course_purchase=purchase.purchase_number, 
                course_date=purchase.purchase_date, 
                course_cost=course.course_cost)
    return course_details 

def mergeOwned(owned: list[UdemyCourseOwn], course_purchase_details: dict):
    """
    Merges purchase information into the Udemy owned courses
    """
    for crs_ind, course in enumerate(owned):
        if course.course_page in course_purchase_details:
            owned[crs_ind].purchase = course_purchase_details[course.course_page]

def processItems(owned: list[UdemyCourseOwn], purchases: list[UdemyPurchase]):
    """
    Processes the owned courses and purchases
    """
    logger.info("Processing Items")
    owned_dict = getOwnedDict(owned)
    processPurchases(purchases, owned_dict)
    course_purchase_details = getCoursePurchaseDetails(purchases)
    mergeOwned(owned, course_purchase_details)
    logger.info("Items Processed")

def toDF(source_list: ExcelOutputable) -> pd.DataFrame:
    """
    Converts Udemy classes into data frames
    """
    return pd.DataFrame([item.toExcelDict() for item in source_list])

def exportAllExcel(owned: list[UdemyCourseOwn], purchases: list[UdemyPurchase]):
    """
    Exports Udemy classes into an Excel file
    """
    logger.info("Exporting to Excel")
    output_path = Path(os.environ.get("OUTPUT_PATH", "Udemy.xlsx"))
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        toDF(purchases).to_excel(writer,
                                 sheet_name="Purchase", 
                                 index=False)
        toDF(owned).to_excel(writer,
                             sheet_name="Course", 
                             index=False)
    logger.info("Exported to Excel")
        