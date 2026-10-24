from udemy_purchase_scraper.config import CONFIG
import requests
import requests.cookies
import json
from seleniumbase import BaseCase
import time
from udemy_purchase_scraper.exceptions import BadCookies
import logging
import os
from typing import Literal

def checkUseHeadless() -> bool:
    """
    Checks environment variables to see if we can run in headless mode
    """
    run_headless = CONFIG.HEADLESS
    force_new_cookies = CONFIG.FORCE_NEW_COOKIES
    headless_status = not force_new_cookies and run_headless
    return headless_status

def saveCookies(sb: BaseCase) -> None:
    '''
    Saves Udemy cookies
    '''
    saved_cookies = sb.get_cookies()
    with open(CONFIG.COOKIES_PATH, "w") as file:
        json.dump(saved_cookies, file)

def loadCookies(sb: BaseCase) -> None:
    '''
    Loads Udemy cookies
    '''
    if not CONFIG.COOKIES_PATH.exists():
        raise BadCookies("Cookies file does not exist")
    with open(CONFIG.COOKIES_PATH, "r") as file:
        saved_cookies = json.load(file)
        sb.add_cookies(saved_cookies)

    time.sleep(1)
    return None

def requestsCookiesFromSelenium() -> requests.cookies.RequestsCookieJar:
    '''
    Turns selenium cookies into cookies for Requests
    '''
    with open(CONFIG.COOKIES_PATH, "r") as file:
        saved_cookies = json.load(file)
    jar = requests.cookies.RequestsCookieJar()
    for cookie in saved_cookies:
        rest = {}
        for key, val in cookie.items():
            if key not in ["name", "value", "domain"]:
                rest[key] = val
        jar.set_cookie(
                requests.cookies.create_cookie(
                    name = cookie.get("name"),
                    value = cookie.get("value"),
                    domain = cookie.get("domain"),
                    rest = rest  
                )
            )
    return jar 

def checkLogLevel(log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]) -> int:
    """
    Checks for the logging level
    """
    return logging.getLevelNamesMapping().get(log_level, logging.INFO)