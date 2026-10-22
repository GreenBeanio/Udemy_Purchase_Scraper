from seleniumbase import BaseCase
from seleniumbase import SB
from seleniumbase.undetected.cdp_driver.element import Element
import datetime
from decimal import Decimal
import os
import time
from udemy_purchase_scraper.exceptions import SingleCourseError, RetryError, LastPageError
from udemy_purchase_scraper.purchase.classes import UdemyPurchase, UdemyCoursePurchase

def getPurchasePage(sb: BaseCase) -> list[Element]:
    '''
    A function to get the purchases from the 'purchase-history' page
    '''
    purchase_table: Element = sb.find_element("table[class*='paginated-table_purchase-history-table']")
    purchases: list[Element] = purchase_table.query_selector_all("tr[class*='paginated-table_purchase-history-table--main-row']")
    return(purchases)

def getPurchaseInformation(purchase: Element, sb: SB) -> UdemyPurchase:
    '''
    
    '''
    purchase_number: Element = purchase.query_selector_all('span.ud-btn-label')
    for c_pur in purchase_number:
        if c_pur.text == "Receipt":
            purchase_number: Element = c_pur
            break
    purchase_number: Element = sb.get_parent(purchase_number)
    purchase_number: str = purchase_number.href
    purchase_number: str = purchase_number.split("/")[-2]
    purchase_cost: str = purchase.query_selector("div[class*='paginated-table_purchase-history-table--data-cell'] > div[class*='app_positive-text']").text
    purchase_cost: Decimal = Decimal(purchase_cost.replace("$","").strip())
    purchase_dates: list[Element] = purchase.query_selector_all("div[class*='paginated-table_purchase-history-table--data-cell']")
    # Could also probably just grab the second index    
    for c_date in purchase_dates:
        if len(c_date.query_selector_all("*")) == 0:
            purchase_date: str = c_date.text
            break
    purchase_date: datetime.date = datetime.datetime.strptime(purchase_date, "%b %d, %Y").date()
    cur_purchase = UdemyPurchase(purchase_number=purchase_number,
                                 purchase_cost= purchase_cost,
                                 purchase_date=purchase_date)
    return(cur_purchase)

def checkMultipleCourses(purchase: Element) -> Element:
    '''
    A function to check if a purchase has multiple courses
    '''
    link_section: Element = purchase.query_selector("div[class*='paginated-table_purchase-details--text-container']")
    show_more_button: Element = link_section.query_selector("button[class*='show-more_focusable-label']")
    if show_more_button is None:
        raise SingleCourseError("Purchase only has a single course")
    return(show_more_button)

def getPurchaseCourseSingle(purchase: Element) -> UdemyCoursePurchase:
    '''
    A function to get the courses from a purchase with a single course
    '''
    course_name_element: Element = purchase.query_selector("div[class*='paginated-table_purchase-details--content-title-text']")
    course_name_element: Element = course_name_element.query_selector("a")
    course_name: str = course_name_element.get_html()
    course_link: str = f"https://www.udemy.com{course_name_element.href}"
    course_price: str = purchase.query_selector("div[class*='app_positive-text']").text
    course_price: Decimal = Decimal(course_price.replace("$","").strip())
    course = UdemyCoursePurchase(course_name=course_name,
                                 course_link=course_link,
                                 course_cost=course_price)
    return(course)

def getPurchaseCourseMultiple(sb: BaseCase) -> list[Element]:
    '''
    A function to get the courses from a purchase with multiple courses
    '''
    courses: list[Element] = sb.find_elements("tr[class*='paginated-table_purchase-history-table--sub-row']")
    courses = [getPurchaseCourseSingle(purchase=course) for course in courses]
    return(courses)

def getPurchaseCourses(purchase: any, sb: BaseCase) -> list[UdemyCoursePurchase]:
    '''
    A function to get the courses in a purchase
    '''
    try:
        expand_purchase = checkMultipleCourses(purchase)
        expand_purchase.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3))/2)
        courses = getPurchaseCourseMultiple(sb=sb)
        expand_purchase.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3))/2)
    except SingleCourseError:
        courses = [getPurchaseCourseSingle(purchase)]
    return(courses)

def getPurchasePageResults(sb: BaseCase) -> list[UdemyPurchase]:
    """
    A function to get the results from a page of purchases
    """
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            purchase_page = getPurchasePage(sb=sb)
            purchases = [None] * len(purchase_page)
            for ind, purchase in enumerate(purchase_page):
                cur_purchase = getPurchaseInformation(purchase=purchase, sb=sb)
                cur_purchase.courses = getPurchaseCourses(purchase=purchase, sb=sb)
                purchases[ind] = cur_purchase
            return(purchases)
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    raise RetryError("Ran out of retries")

def checkMorePurchases(sb: BaseCase) -> None:
    '''
    A function to check if a purchase has multiple courses
    '''
    try:
        next_page: Element = sb.find_element("a[class*=pagination_next][aria-label='next page'][aria-disabled='false']")
        next_page.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    except:
        raise LastPageError("No more purchase pages")


def getPurchasePages(sb: BaseCase) -> list[UdemyPurchase]:
    """
    A function to get the purchase results from all pages
    """
    sb.goto("https://www.udemy.com/dashboard/purchase-history/")
    time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    purchases: list[UdemyPurchase] = []
    while True:
        page_results = getPurchasePageResults(sb)
        purchases.extend(page_results)
        try:
            checkMorePurchases(sb=sb)
        except LastPageError:
            break
    return(purchases)