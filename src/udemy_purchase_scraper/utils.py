import requests
import requests.cookies
import json
import os
from seleniumbase import BaseCase
import time
from udemy_purchase_scraper.exceptions import BadCookies
from pathlib import Path
import logging

def checkForceNewCookies() -> bool:
    """
    Checks for the FORCE_NEW_COOKIES environment variable
    """
    force_new_cookies = os.environ.get("FORCE_NEW_COOKIES", False)
    if isinstance(force_new_cookies, str):
        if force_new_cookies.lower() == "false":
            force_new_cookies = False
        elif force_new_cookies.lower() == "true":
            force_new_cookies = True
        else:
            force_new_cookies = False
    return force_new_cookies 

def checkHeadless() -> bool:
    """
    Checks for the HEADLESS environment variable
    """
    run_headless = os.environ.get("HEADLESS", False)
    if isinstance(run_headless, str):
        run_headless = run_headless.lower() == "true"
    return run_headless 

def checkUseHeadless() -> bool:
    """
    Checks environment variables to see if we can run in headless mode
    """
    run_headless = checkHeadless()
    force_new_cookies = checkForceNewCookies()
    headless_status = not force_new_cookies and run_headless
    return headless_status 

def checkChromeVersion() -> int|None:
    """
    Checks for the CHROME_VERSION environment variable
    """
    chrome_version = os.environ.get("CHROME_VERSION", None)
    if isinstance(chrome_version, str):
        if chrome_version.lower() == "none":
            chrome_version = None
        else:
            try:
                chrome_version = int(chrome_version)
            except:
                chrome_version = None
    return chrome_version 

def saveCookies(sb: BaseCase) -> None:
    '''
    Saves Udemy cookies
    '''
    cookies_path = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
    saved_cookies = sb.get_cookies()
    with open(cookies_path, "w") as file:
        json.dump(saved_cookies, file)

def loadCookies(sb: BaseCase) -> None:
    '''
    Loads Udemy cookies
    '''
    cookies_path = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
    if not cookies_path.exists():
        raise BadCookies("Cookies file does not exist")
    with open(cookies_path, "r") as file:
        saved_cookies = json.load(file)
        sb.add_cookies(saved_cookies)

    time.sleep(1)
    return None

def requestsCookiesFromSelenium() -> requests.cookies.RequestsCookieJar:
    '''
    Turns selenium cookies into cookies for Requests
    '''
    cookies_path = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
    with open(cookies_path, "r") as file:
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

def checkLogLevel() -> logging._Level:
    """
    Checks for the logging level
    """
    return logging.getLevelNamesMapping().get(os.environ.get("LOG_LVL", "INFO").upper(), logging.INFO)