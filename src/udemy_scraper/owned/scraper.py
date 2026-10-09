from undetected_chromedriver import By
import os
import time
import re
import src.udemy_scraper.exceptions as u_ec
import udemy_scraper.owned.classes as u_o_cl

def getOwnedInformation(course: any) -> any:
    '''
    
    '''
    course_info = course.find_element(By.XPATH,".//h3[@data-purpose='course-title-url']//a")
    course_title = course_info.text
    course_link = course_info.get_attribute("href")
    instructor = course.find_element(By.XPATH, ".//div[@class='course-card-instructors-module--instructor-list--cJTfw']").text
    instructor = re.split(r"[,\|•-]", instructor)[0].strip()
    cur_purchase = u_o_cl.UdemyCourseOwn(course_name=course_title,
                                         course_link=course_link,
                                         course_author=instructor)
    return(cur_purchase)

def getOwnedPage(driver: any) -> any:
    '''
    
    '''
    courses_grid = driver.find_element(By.XPATH, "//div[@class='my-courses__course-card-grid']")
    courses = courses_grid.find_elements(By.XPATH, "./div")
    courses = [getOwnedInformation(course=course) for course in courses]
    return(courses)

def checkMoreOwned(driver: any) -> None:
    '''
    
    '''
    try:
        next_page = driver.find_element(By.XPATH, ".//a[@class='ud-btn ud-btn-medium ud-btn-secondary ud-btn-round ud-btn-text-sm ud-btn-icon ud-btn-icon-medium ud-btn-icon-round pagination-module--next--QX6nm'" \
                                        " and @aria-label='next page' " \
                                        "and @aria-disabled='false']")
        next_page.click()
        time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    except:
        raise u_ec.LastPageError("No more owned pages")

def getOwnedResults(driver: any) -> any:
    """
    
    """
    retry = 0
    while retry < int(os.environ.get("RETRY_LIMIT", 3)):
        try:
            page_results = getOwnedPage(driver=driver)
            return(page_results)
        except:
            retry += 1
            time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    raise u_ec.RetryError("Ran out of retries")

def getOwnedPages(driver: any) -> any:
    """
    
    """
    driver.get("https://www.udemy.com/home/my-courses/learning/?sort=-enroll_time")
    time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    courses = []
    while True:
        page_results = getOwnedResults(driver=driver)
        courses.extend(page_results)
        try:
            checkMoreOwned(driver=driver)
        except u_ec.LastPageError:
            break
    return(courses)

def getOwnedCurrentURL(driver: any, course_link: str):
    """
    x
    """
    driver.get(course_link)
    #time.sleep(int(os.environ.get("SLEEP_TIME", 3)))
    return(driver.current_url.split("/learn")[0])

def getOwnedCurrentURLRequest(session: any, course_link: str):
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