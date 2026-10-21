from seleniumbase import BaseCase
#from selenium.webdriver.remote.webelement import WebElement
from seleniumbase.undetected.cdp_driver.element import Element
import os
import time
import re
import udemy_purchase_scraper.exceptions as u_ec
import udemy_purchase_scraper.owned.classes as u_o_cl
import requests

def getOwnedInformation(course: Element) -> u_o_cl.UdemyCourseOwn:
    '''
    
    '''
    #course_info: WebElement = course.find_element(".//h3[@data-purpose='course-title-url']//a")
    course_info: Element = course.query_selector("h3[data-purpose='course-title-url'] a")
    course_title = course_info.text
    #course_link = course_info.get_attribute("href")
    course_link = course_info.href
    #instructor: WebElement = course.find_element(".//div[@class='course-card-instructors-module--instructor-list--cJTfw']").text
    instructor: Element = course.query_selector("div[class*='course-card-instructors-module--instructor-list']").text
    instructor = re.split(r"[,\|•-]", instructor)[0].strip()
    cur_purchase = u_o_cl.UdemyCourseOwn(course_name=course_title,
                                         course_link=course_link,
                                         course_author=instructor)
    return(cur_purchase)

def getOwnedPage(sb: BaseCase) -> list[u_o_cl.UdemyCourseOwn]:
    '''
    
    '''
    #courses_grid: WebElement = sb.find_element("//div[@class='my-courses__course-card-grid']")
    courses_grid: Element = sb.find_element("div[class='my-courses__course-card-grid']")
    #courses: list[WebElement] = courses_grid.find_elements("./div")
    courses: list[Element] = courses_grid.query_selector_all(":scope > div")
    #courses: list[Element] = courses_grid.query_selector_all("div[class='my-courses__course-card-grid'] > div")
    print(len(courses))
    courses = [getOwnedInformation(course=course) for course in courses]
    return(courses)

def checkMoreOwned(sb: BaseCase) -> Element:
    '''
    
    '''
    try:
        #next_page: WebElement = sb.find_element(".//a[@class='ud-btn ud-btn-medium ud-btn-secondary ud-btn-round ud-btn-text-sm ud-btn-icon ud-btn-icon-medium ud-btn-icon-round pagination-module--next--QX6nm' and @aria-label='next page' and @aria-disabled='false']")
        next_page: Element = sb.find_element("a[class*=pagination-module--next][aria-label='next page'][aria-disabled='false']")
        next_page.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    except:
        raise u_ec.LastPageError("No more owned pages")

def getOwnedResults(sb: BaseCase) -> list[u_o_cl.UdemyCourseOwn]:
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
    raise u_ec.RetryError("Ran out of retries")

def getOwnedPages(sb: BaseCase) -> list[u_o_cl.UdemyCourseOwn]:
    """
    
    """
    sb.get("https://www.udemy.com/home/my-courses/learning/?sort=-enroll_time")
    time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    courses = []
    while True:
        page_results = getOwnedResults(sb=sb)
        courses.extend(page_results)
        try:
            checkMoreOwned(sb=sb)
        except u_ec.LastPageError:
            break
    return(courses)

def getOwnedCurrentURL(sb: BaseCase, course_link: str) -> str:
    """
    x
    """
    sb.get(course_link)
    #time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    return(sb.current_url.split("/learn")[0])

def getOwnedCurrentURLRequest(session: requests.Session, course_link: str) -> str:
    """
    x
    """
    # #response = session.get(course_link, cookies=jar).url
    # #response = session.head(course_link, allow_redirects=True).url
    # response = session.head(course_link, allow_redirects=True)
    # print(response.status_code)
    # #time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    # #return(response.split("/learn")[0])
    # return(response.url.split("/learn")[0])
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            response = session.head(course_link, allow_redirects=True)
            response.raise_for_status()
            return(response.url.split("/learn/")[0])
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    raise u_ec.RetryError("Ran out of retries")