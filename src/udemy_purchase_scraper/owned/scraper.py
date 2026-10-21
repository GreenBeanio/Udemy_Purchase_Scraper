from seleniumbase import BaseCase
from seleniumbase.undetected.cdp_driver.element import Element
import os
import time
import re
from udemy_purchase_scraper.exceptions import LastPageError, RetryError
from udemy_purchase_scraper.owned.classes import UdemyCourseOwn
import requests

def getOwnedInformation(course: Element) -> UdemyCourseOwn:
    '''
    
    '''
    course_info: Element = course.query_selector("h3[data-purpose='course-title-url'] a")
    course_title = course_info.text
    course_link = course_info.href
    instructor: Element = course.query_selector("div[class*='course-card-instructors-module--instructor-list']").text
    instructor = re.split(r"[,\|•-]", instructor)[0].strip()
    cur_purchase = UdemyCourseOwn(course_name=course_title,
                                         course_link=course_link,
                                         course_author=instructor)
    return(cur_purchase)

def getOwnedPage(sb: BaseCase) -> list[UdemyCourseOwn]:
    '''
    
    '''
    courses_grid: Element = sb.find_element("div[class='my-courses__course-card-grid']")
    courses: list[Element] = courses_grid.query_selector_all(":scope > div")
    courses = [getOwnedInformation(course=course) for course in courses]
    return(courses)

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
            return(page_results)
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    raise RetryError("Ran out of retries")

def getOwnedPages(sb: BaseCase) -> list[UdemyCourseOwn]:
    """
    
    """
    sb.goto("https://www.udemy.com/home/my-courses/learning/?sort=-enroll_time")
    time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    courses = []
    while True:
        page_results = getOwnedResults(sb=sb)
        courses.extend(page_results)
        try:
            checkMoreOwned(sb=sb)
        except LastPageError:
            break
    return(courses)

def getOwnedCurrentURL(sb: BaseCase, course_link: str) -> str:
    """
    x
    """
    sb.goto(course_link)
    return(sb.current_url.split("/learn")[0])

def getOwnedCurrentURLRequest(session: requests.Session, course_link: str) -> str:
    """
    x
    """
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            response = session.head(course_link, allow_redirects=True)
            response.raise_for_status()
            return(response.url.split("/learn/")[0])
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    raise RetryError("Ran out of retries")