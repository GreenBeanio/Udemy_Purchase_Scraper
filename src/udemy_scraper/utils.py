import requests
import json
import os
import undetected_chromedriver as uc
import time

def checkForceNewCookies():
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

def saveCookies(driver: uc.Chrome, f_path: str, force_cookies: bool = True) -> None:
    '''
    Saves the cookies from your udemy in

    :param driver: The web driver
    :type driver: Chrome

    :param f_path: The file name (or full file path)
    :type f_path: str

    :param force_cookies: If we force the cookies even if they already exist, defaults to [True]
    :type force_cookies: bool

    :return: Nothing
    :rtype: None
    '''
    # Checking if the cookies file already exists
    if(force_cookies or not os.path.exists(f_path)):
        # Wait for an input for the user to log in
        input("Continue after you've logged into Udemy!")
        # To save cookies
        saved_cookies = driver.get_cookies()
        with open(f_path, "w") as file:
            json.dump(saved_cookies, file)
    return None

def loadCookies(driver: uc.Chrome, f_path: str):
    '''
    Loads your Udemy cookies in

    :param driver: The web driver
    :type driver: Chrome

    :param f_path: The file name (or full file path)
    :type f_path: str

    :return: Nothing
    :rtype: None
    '''
    # To load in cookies
    with open(f_path, "r") as file:
        saved_cookies = json.load(file)
    for x in saved_cookies:
        driver.add_cookie(x)
    # Wait for one second just to be sure (probably not needed)
    time.sleep(1)
    return None

def requestsCookiesFromSelenium(cookies_file: str) -> any: #selenium_cookies: dict) -> any:
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
                    #expiry = cookie.get("expiry"),
                    #httpOnly = cookie.get("httpOnly"),
                    #path = cookie.get("path"),
                    #sameSite = cookie.get("sameSite"),
                    #secure = cookie.get("secure")
                    rest = rest  
                )
            )
    return(jar)