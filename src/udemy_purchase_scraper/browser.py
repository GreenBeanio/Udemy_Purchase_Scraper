from seleniumbase import Driver
import udemy_purchase_scraper.utils as us_u

def startBrowser():
    """
    x
    """
    is_headless = us_u.checkForcedHeadless()
    chrome_version = us_u.checkChromeVersion()
    driver = Driver(
        #browser="chrome",
        #incognito=True,
        uc=True, # Undetected Mode
        headed=is_headless, # Headless mode,
        driver_version=chrome_version # A version to pin if needed
    )
    if is_headless:
        driver.set_window_size(1920, 1080)
    else:
        driver.maximize_window()
    return(driver)