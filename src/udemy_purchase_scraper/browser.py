from udemy_purchase_scraper.config import CONFIG
from seleniumbase import SB
from udemy_purchase_scraper.utils import checkUseHeadless
from contextlib import contextmanager
from collections.abc import Generator

@contextmanager
def startBrowser(is_headless: bool = None, driver_list: list = None) -> Generator[SB, None, None]:
    """
    Starts a Selenium browser instance
    """
    if is_headless is None:
          is_headless = checkUseHeadless()
    if is_headless:
        with SB(
                incognito=True, # Hides past session/profile info
                uc=True, # Undetected Mode
                xvfb=is_headless, # Headless mode,
                headless2=is_headless, # Improved headless mode,
                driver_version=CONFIG.CHROME_VERSION, # A version to pin if needed
                window_size="1920, 1080"
            ) as sb:
                if driver_list is not None:
                      driver_list.append(sb.driver)
                try:
                    yield(sb)
                finally:
                      if driver_list is not None and sb.driver in driver_list:
                            driver_list.remove(sb.driver)
    else:
        with SB(
                incognito=True, # Hides past session/profile info
                uc=True, # Undetected Mode
                driver_version=CONFIG.CHROME_VERSION, # A version to pin if needed
                window_position="0, 0"
            ) as sb:
                if driver_list is not None:
                    driver_list.append(sb.driver)
                try:
                    yield(sb)
                finally:
                        if driver_list is not None and sb.driver in driver_list:
                            driver_list.remove(sb.driver)