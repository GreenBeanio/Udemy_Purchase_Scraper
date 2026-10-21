from seleniumbase import SB
import udemy_purchase_scraper.utils as us_u
from contextlib import contextmanager
from collections.abc import Generator

@contextmanager
def startBrowser() -> Generator[SB, None, None]:
    """
    x
    """
    is_headless = us_u.checkUseHeadless()
    chrome_version = us_u.checkChromeVersion()
    if is_headless:
        with SB(
                incognito=True, # Hides past session/profile info
                uc=True, # Undetected Mode
                xvfb=is_headless, # Headless mode,
                headless2=is_headless, # Improved headless mode,
                driver_version=chrome_version, # A version to pin if needed
                window_size="1920, 1080"
            ) as sb:
                yield(sb)
    else:
        with SB(
                incognito=True, # Hides past session/profile info
                uc=True, # Undetected Mode
                driver_version=chrome_version, # A version to pin if needed
                window_position="0, 0"
            ) as sb:
                yield(sb)