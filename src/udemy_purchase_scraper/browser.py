from seleniumbase import Driver
import udemy_purchase_scraper.utils as us_u
import os

def startBrowser():
    """
    x
    """
    is_headless = us_u.checkForcedHeadless()
    chrome_version = us_u.checkChromeVersion()
    driver = Driver(
        uc=True, # Undetected Mode
        headed=is_headless, # Headless mode,
        driver_version=chrome_version, # A version to pin if needed
        no_sandbox=True, # Run the same as a user instead of sandboxing
        disable_gpu=not is_headless # Works better when headless
    )
    if is_headless:
        driver.set_window_size(1920, 1080)
    else:
        driver.maximize_window()
    return(driver)