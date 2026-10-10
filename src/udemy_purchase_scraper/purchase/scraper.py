from seleniumbase import BaseCase
from selenium.webdriver.remote.webelement import WebElement
import datetime
from decimal import Decimal
import os
import time
import src.udemy_purchase_scraper.exceptions as u_ec
import udemy_purchase_scraper.purchase.classes as u_p_cl

def getPurchasePage(sb: BaseCase) -> list[WebElement]:
    '''
    A function to get the purchases from the 'purchase-history' page
    '''
    purchase_table: WebElement = sb.find_element("//table[@class='paginated-table_purchase-history-table__ncCll']")
    purchases: list[WebElement] = purchase_table.find_elements(".//tr[@class='paginated-table_purchase-history-table--main-row__5hHCb']")
    return purchases

def getPurchaseInformation(purchase: BaseCase) -> u_p_cl.UdemyPurchase:
    '''
    
    '''
    purchase_number: WebElement = purchase.find_element(".//span[@class='ud-btn-label' and contains(., 'Receipt')]")
    purchase_number: WebElement = purchase_number.find_element("..")
    purchase_number: str = purchase_number.get_attribute("href")
    purchase_number: str = purchase_number.split("/")[-2]

    purchase_cost: str = purchase.find_element(".//div[@class='paginated-table_purchase-history-table--data-cell__LO_7L']/div[@class='app_positive-text___Wb07']").text
    purchase_cost: Decimal = Decimal(purchase_cost.replace("$","").strip())

    purchase_date: str = purchase.find_element(".//div[@class='paginated-table_purchase-history-table--data-cell__LO_7L' and not(descendant::*)]").text
    purchase_date: datetime.date = datetime.datetime.strptime(purchase_date, "%b %d, %Y").date()

    cur_purchase = u_p_cl.UdemyPurchase(purchase_number=purchase_number,
                                        purchase_cost= purchase_cost,
                                        purchase_date=purchase_date)
    return(cur_purchase)

def checkMultipleCourses(purchase: BaseCase) -> WebElement:
    '''
    A function to check if a purchase has multiple courses
    '''
    try:
        link_section: WebElement = purchase.find_element(".//div[@class='paginated-table_purchase-details--text-container__EvFRz']")
        show_more_button: WebElement = link_section.find_element(".//button[@class='ud-btn ud-btn-medium ud-btn-link ud-btn-text-sm show-more_focusable-label__dmEhW']")
        return(show_more_button)
    except:
        raise u_ec.SingleCourseError("Purchase only has a single course")

def getPurchaseCourseSingle(purchase: BaseCase) -> u_p_cl.UdemyCoursePurchase:
    '''
    A function to get the courses from a purchase with a single course
    '''
    course_name_element: WebElement = purchase.find_element(".//div[@class='paginated-table_purchase-details--text__JKVm6 paginated-table_purchase-details--content-title-text__DxDuf ud-text-md']")
    course_name_element: WebElement = course_name_element.find_element(".//a")

    course_name: str = course_name_element.get_attribute("innerHTML")
    course_link: str = course_name_element.get_attribute("href")
    
    course_price: str = purchase.find_element(".//div[@class='app_positive-text___Wb07']").text
    course_price: Decimal = Decimal(course_price.replace("$","").strip())
    
    course = u_p_cl.UdemyCoursePurchase(course_name=course_name,
                                        course_link=course_link,
                                        course_cost=course_price)
    return(course)

def getPurchaseCourseMultiple(sb: BaseCase) -> list[WebElement]:
    '''
    A function to get the courses from a purchase with multiple courses
    '''
    courses: list[WebElement] = sb.find_elements(".//tr[@class='paginated-table_purchase-history-table--sub-row__2g87b']")
    courses = [getPurchaseCourseSingle(purchase=course) for course in courses]
    return(courses)

def getPurchaseCourses(purchase: any, sb: BaseCase) -> list[u_p_cl.UdemyCoursePurchase]:
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
    except u_ec.SingleCourseError:
        courses = [getPurchaseCourseSingle(purchase)]
    return(courses)

def getPurchasePageResults(sb: BaseCase) -> list[u_p_cl.UdemyPurchase]:
    """
    A function to get the results from a page of purchases
    """
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            purchase_page = getPurchasePage(sb=sb)
            purchases = [None] * len(purchase_page)
            for ind, purchase in enumerate(purchase_page):
                cur_purchase = getPurchaseInformation(purchase=purchase)
                cur_purchase.courses = getPurchaseCourses(purchase=purchase, sb=sb)
                purchases[ind] = cur_purchase
            return(purchases)
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    raise u_ec.RetryError("Ran out of retries")

def checkMorePurchases(sb: BaseCase) -> None:
    '''
    A function to check if a purchase has multiple courses
    '''
    try:
        next_page: WebElement = sb.find_element(".//a[@class='ud-btn ud-btn-medium ud-btn-secondary ud-btn-round ud-btn-text-sm ud-btn-icon ud-btn-icon-medium ud-btn-icon-round pagination_next__aBqfT' " \
                                                    "and @aria-label='next page' " \
                                                    "and @aria-disabled='false']")
        next_page.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    except:
        raise u_ec.LastPageError("No more purchase pages")

def getPurchasePages(sb: BaseCase) -> list[u_p_cl.UdemyPurchase]:
    """
    A function to get the purchase results from all pages
    """
    sb.get("https://www.udemy.com/dashboard/purchase-history/")
    time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    purchases: list[u_p_cl.UdemyPurchase] = []
    while True:
        page_results = getPurchasePageResults(sb)
        #purchases.append(page_results)
        purchases.extend(page_results)
        try:
            checkMorePurchases(sb=sb)
        except u_ec.LastPageError:
            break
    return(purchases)