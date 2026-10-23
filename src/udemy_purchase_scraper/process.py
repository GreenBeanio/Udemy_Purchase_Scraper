from udemy_purchase_scraper.owned.classes import UdemyCoursePurchaseDetails
from udemy_purchase_scraper.protocols import ExcelOutputable
import pandas as pd
import os
from pathlib import Path
from typing import Literal

def getOwnedDict(owned: any):
    owned_dict = {}
    for course in owned:
        owned_dict[course.course_page] = course
    return owned_dict 

def getPurchaseDict(purchases: any):
    purchase_dict = {}
    for purchase in purchases:
        for course in purchase.courses:
            purchase_dict[course.course_link] = None
    return purchase_dict 

def findFreeCourses(owned_dict, purchase_dict):
    missing_owned_courses = set(owned_dict.keys()).difference(set(purchase_dict.keys()))
    free_courses = [owned_dict[course] for course in missing_owned_courses]
    return free_courses 

def recalculatePurchases(purchases, owned_dict):
    original_lengths = [len(purchase.courses) for purchase in purchases]
    purchase_dict = {}
    for purchase in purchases:
        purchase.courses = [course for course in purchase.courses if course.course_link in owned_dict and course.course_link not in purchase_dict]
        for course in purchase.courses:
            purchase_dict[course.course_link] = None
    new_lengths = [len(purchase.courses) for purchase in purchases]
    for ind, purchase in enumerate(purchases):
        if original_lengths[ind] != new_lengths[ind] and new_lengths[ind] != 0:
            purchases[ind].purchase_cost = sum([course.course_cost for course in purchases[ind].courses])
    purchases = [purchase for purchase in purchases if len(purchase.courses) != 0]
    return purchases 

def getCoursePurchaseDetails(purchases):
    course_details = {}
    for purchase in purchases:
        for course in purchase.courses:
            course_details[course.course_link] = UdemyCoursePurchaseDetails(
                course_purchase=purchase.purchase_number, 
                course_date=purchase.purchase_date, 
                course_cost=course.course_cost)
    return course_details 

def mergeOwned(owned, course_purchase_details):
    for crs_ind, course in enumerate(owned):
        if course.course_page in course_purchase_details:
            owned[crs_ind].purchase = course_purchase_details[course.course_page]

def mergePurchases(purchases, course_purchase_details):
    for p_ind, purchase in enumerate(purchases):
        for c_ind, course in enumerate(purchase.courses):
            purchases[p_ind].courses[c_ind] = course_purchase_details[course.course_link]

def processItems(owned, purchases):
    owned_dict = getOwnedDict(owned)
    #purchase_dict = getPurchaseDict(purchases)
    #free_dict = findFreeCourses(owned_dict, purchase_dict)
    recalculatePurchases(purchases, owned_dict)
    course_purchase_details = getCoursePurchaseDetails(purchases)
    mergeOwned(owned, course_purchase_details)
    #mergePurchases(purchases, course_purchase_details)

def toDF(source_list: ExcelOutputable) -> pd.DataFrame:
    """
    x
    """
    return pd.DataFrame([item.toExcelDict() for item in source_list])

def exportExcel(df: pd.DataFrame, sheet_name = Literal["Purchase", "Course"]):
    """
    x
    """
    output_path = Path(os.environ.get("OUTPUT_PATH", "Udemy.xlsx"))
    df.to_excel(output_path, 
                sheet_name=sheet_name, 
                index=False, 
                engine="openpyxl")

def exportAllExcel(owned, purchases):
    """
    x
    """
    output_path = Path(os.environ.get("OUTPUT_PATH", "Udemy.xlsx"))
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        toDF(purchases).to_excel(writer,
                                 sheet_name="Purchase", 
                                 index=False)
        toDF(owned).to_excel(writer,
                             sheet_name="Course", 
                             index=False)
        