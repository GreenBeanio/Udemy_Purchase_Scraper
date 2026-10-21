import requests
import requests.cookies
import json
import os
from seleniumbase import BaseCase
import time
import pickle
import udemy_purchase_scraper.purchase.classes as u_p_cl
import udemy_purchase_scraper.owned.classes as u_o_cl
import udemy_purchase_scraper.exceptions as u_ec
from pathlib import Path

def checkForceNewCookies() -> bool:
    """
    x
    """
    force_new_cookies = os.environ.get("FORCE_NEW_COOKIES", False)
    if isinstance(force_new_cookies, str):
        if force_new_cookies.lower() == "false":
            force_new_cookies = False
        elif force_new_cookies.lower() == "true":
            force_new_cookies = True
        else:
            force_new_cookies = False
    return(force_new_cookies)

def checkHeadless() -> bool:
    """
    x
    """
    run_headless = os.environ.get("HEADLESS", False)
    if isinstance(run_headless, str):
        run_headless = run_headless.lower() == "true"
    return(run_headless)

def checkUseHeadless() -> bool:
    """
    x
    """
    run_headless = checkHeadless()
    force_new_cookies = checkForceNewCookies()
    headless_status = not force_new_cookies and run_headless
    return(headless_status)

def checkChromeVersion() -> int|None:
    """
    x
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
    return(chrome_version)

def saveCookies(sb: BaseCase) -> None:
    '''
    Saves the cookies from your udemy in

    :param driver: The web driver
    :type driver: Chrome

    :return: Nothing
    :rtype: None
    '''
    cookies_path = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
    saved_cookies = sb.get_cookies()
    with open(cookies_path, "w") as file:
        json.dump(saved_cookies, file)

def loadCookies(sb: BaseCase) -> None:
    '''
    Loads your Udemy cookies in

    :param driver: The web driver
    :type driver: Chrome

    :return: Nothing
    :rtype: None
    '''
    cookies_path = Path(os.environ.get("COOKIES_PATH", "cookies.json"))
    if not cookies_path.exists():
        raise u_ec.BadCookies("Cookies file does not exist")
    with open(cookies_path, "r") as file:
        saved_cookies = json.load(file)
        sb.add_cookies(saved_cookies)

    time.sleep(1)
    return None

def requestsCookiesFromSelenium(cookies_file: str) -> requests.cookies.RequestsCookieJar:
    '''
    x
    '''
    with open(cookies_file, "r") as file:
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
    return(jar)

def savePurchases(purchase_data: list[u_p_cl.UdemyPurchase]) -> None:
    '''
    x
    '''
    data_path = Path(os.environ.get("PUR_PATH", "purchases.pkl"))
    with open(data_path, "wb") as save_file:
        pickle.dump(purchase_data, save_file)

def saveOwned(owned_data: list[u_o_cl.UdemyCourseOwn]) -> None:
    '''
    x
    '''
    data_path = Path(os.environ.get("OWN_PATH", "owned.pkl"))
    with open(data_path, "wb") as save_file:
        pickle.dump(owned_data, save_file)

def loadPurchases() -> list[u_p_cl.UdemyPurchase]:
    '''
    x
    '''
    data_path = Path(os.environ.get("PUR_PATH", "purchases.pkl"))
    if not os.path.exists(data_path):
        raise FileNotFoundError("Purchases file does not exist")
    with open("backup_data.pkl", "rb") as load_file:
        data_load = pickle.load(load_file)
        return(data_load)

def loadOwned() -> list[u_o_cl.UdemyCourseOwn]:
    '''
    x
    '''
    data_path = Path(os.environ.get("OWN_PATH", "purchases.pkl"))
    if not os.path.exists(data_path):
        raise FileNotFoundError("Owned file does not exist")

    with open("backup_data.pkl", "rb") as load_file:
        data_load = pickle.load(load_file)
        return(data_load)