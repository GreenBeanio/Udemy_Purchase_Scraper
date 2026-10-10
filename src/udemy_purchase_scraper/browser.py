from seleniumbase import SB, BaseCase
import udemy_purchase_scraper.utils as us_u

def startBrowser() -> BaseCase:
    """
    x
    """
    is_headless = us_u.checkForcedHeadless()
    chrome_version = us_u.checkChromeVersion()
    manager = SB(
        #browser="chrome",
        #incognito=True,
        uc=True, # Undetected Mode
        headed=is_headless, # Headless mode,
        driver_version=chrome_version # A version to pin if needed
    )
    sb = manager.__enter__()
    if is_headless:
        sb.set_window_size(1920, 1080)
    else:
        sb.maximize_window()
    return(sb)