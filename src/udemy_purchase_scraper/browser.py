import undetected_chromedriver as uc
import udemy_purchase_scraper.utils as us_u
import os

def startBrowser():
    """
    x
    """
    # Options for selenium
    options = uc.ChromeOptions()

    run_headless = os.environ.get("HEADLESS", False)
    if run_headless is not False:
        if run_headless.lower == "true":
            run_headless = True
        else:
            run_headless = False

    force_new_cookies = us_u.checkForceNewCookies()
    if force_new_cookies or run_headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    chrome_version = os.environ.get("CHROME_VERSION", None)
    if chrome_version is not None:
        if chrome_version.lower == "none":
            chrome_version = None
        else:
            try:
                chrome_version = int(chrome_version)
            except:
                chrome_version = None
    if chrome_version is not None:
        driver = uc.Chrome(use_subprocess=False, options=options, version_main=chrome_version)
    else:
        driver = uc.Chrome(use_subprocess=False, options=options)
    return(driver)