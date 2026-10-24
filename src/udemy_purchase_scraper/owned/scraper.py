from seleniumbase import BaseCase
from seleniumbase.undetected.cdp_driver.element import Element
import os
import time
import re
from udemy_purchase_scraper.exceptions import LastPageError, RetryError
from udemy_purchase_scraper.owned.classes import UdemyCourseOwn
import requests
from udemy_purchase_scraper.utils import requestsCookiesFromSelenium
import logging

logger = logging.getLogger(__name__)

def getOwnedInformation(course: Element) -> UdemyCourseOwn:
    '''
    
    '''
    course_info: Element = course.query_selector("h3[data-purpose='course-title-url'] a")
    course_title = course_info.text
    course_link = f"https://www.udemy.com{course_info.href}"
    instructor: Element = course.query_selector("div[class*='course-card-instructors-module--instructor-list']").text
    instructor = re.split(r"[,\|•-]", instructor)[0].strip()
    cur_purchase = UdemyCourseOwn(course_name=course_title,
                                         course_link=course_link,
                                         course_author=instructor)
    return cur_purchase 

def getOwnedPage(sb: BaseCase) -> list[UdemyCourseOwn]:
    '''
    
    '''
    courses_grid: Element = sb.find_element("div[class='my-courses__course-card-grid']")
    courses: list[Element] = courses_grid.query_selector_all(":scope > div")
    courses = [getOwnedInformation(course=course) for course in courses]
    return courses 

def checkMoreOwned(sb: BaseCase) -> Element:
    '''
    
    '''
    try:
        next_page: Element = sb.find_element("a[class*=pagination-module--next][aria-label='next page'][aria-disabled='false']")
        next_page.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    except:
        raise LastPageError("No more owned pages")

def getOwnedResults(sb: BaseCase) -> list[UdemyCourseOwn]:
    """
    
    """
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            page_results = getOwnedPage(sb=sb)
            return page_results 
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    logger.critical("Ran out of scrape attempts in getOwnedResults")
    raise RetryError("Ran out of retries")

def getOwnedPages(sb: BaseCase) -> list[UdemyCourseOwn]:
    """
    
    """
    sb.goto("https://www.udemy.com/home/my-courses/learning/?sort=-enroll_time")
    time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    courses_dict = {}
    courses = []
    count = 0
    while True:
        count = count + 1
        page_results = getOwnedResults(sb=sb)
        page_results = [course for course in page_results if course.course_link not in courses_dict]
        for course in page_results:
            courses_dict[course.course_link] = None
        courses.extend(page_results)
        logger.info(f"Finished Owned Page: {count}")
        try:
            checkMoreOwned(sb=sb)
        except LastPageError:
            break
    courses.reverse() # Need to reverse to be oldest to newest
    logger.info("Finished Owned Pages")
    return courses

def getOwnedCurrentURLRequest(session: requests.Session, course_link: str) -> str:
    """
    x
    """
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            response = session.head(course_link, allow_redirects=True)
            response.raise_for_status()
            return response.url.split("/learn/")[0] 
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    logger.critical("Ran out of scrape attempts in getOwnedCurrentURLRequest")
    raise RetryError("Ran out of retries")

def getOwnedCurrentURLs(owned: list[UdemyCourseOwn]) -> list[UdemyCourseOwn]:
    """
    x
    """
    requests_cookies = requestsCookiesFromSelenium()
    with requests.Session() as session:
        session.cookies = requests_cookies
        for ind, course in enumerate(owned):
            owned[ind].course_page = f"{getOwnedCurrentURLRequest(session=session, course_link=course.course_link)}/"
            logger.info(f"Finished Owned URL: {ind+1}")
    logger.info("Finished Owned URLs")