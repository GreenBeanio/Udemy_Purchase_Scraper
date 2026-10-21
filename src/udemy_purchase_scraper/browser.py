from seleniumbase import SB, BaseCase
import udemy_purchase_scraper.utils as us_u
from contextlib import contextmanager
from collections.abc import Generator
import time

@contextmanager
def startBrowser() -> Generator[SB, None, None]:
    """
    x
    """
    is_headless = us_u.checkUseHeadless()
    chrome_version = us_u.checkChromeVersion()
    if is_headless:
        print("no show")
        with SB(
                #browser="chrome", # Sets Chrome, default in uc mode
                incognito=True, # Hides past session/profile info
                uc=True, # Undetected Mode
                xvfb=is_headless, # Headless mode,
                #headless=is_headless, # Headless mode,
                headless2=is_headless, # Improved headless mode,
                driver_version=chrome_version, # A version to pin if needed
                window_size="1920, 1080"
                #window_position="-2500, -2500", # Last resort to be pseudo-headless
            ) as sb:
                yield(sb)
    else:
        print("show")
        with SB(
                #browser="chrome", # Sets Chrome, default in uc mode
                incognito=True, # Hides past session/profile info
                uc=True, # Undetected Mode
                #headless=is_headless, # Headless mode,
                driver_version=chrome_version, # A version to pin if needed
                window_position="0, 0"
            ) as sb:
                yield(sb)
    # with SB(
    #         #browser="chrome",
    #         #incognito=True,
    #         uc=True, # Undetected Mode
    #         xvfb=is_headless, # Headless mode,
    #         #headless=is_headless, # Headless mode,
    #         driver_version=chrome_version # A version to pin if needed
    #     ) as sb:
    #         if is_headless:
    #             print("No show")
    #              # Apparently headless doesn't actually work properly with UC and cdp. On Linux xvfb will push it to a virtual display
    #             # on Windows I'll just automatically minimize it.
    #             sb.set_window_size(1920, 1080)
    #             #sb.set_window_position(-2500, -2500)
    #             sb.minimize()
    #         else:
    #             print("Show")
    #             #sb.maximize_window()
    #             sb.set_window_size(1920, 1080)
    #         #sb.activate_cdp_mode()
    #         yield(sb)