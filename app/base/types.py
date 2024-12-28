from typing import Any

from playwright.sync_api._generated import Browser, Page
from playwright.sync_api import Playwright

Path = str

# typing for PlayWright class
Config = dict[str, Any]
Driver = Playwright
Browser = Browser
ScreenSavePath = Path
PageLocator = str
PlaywrightConfig = dict[str, Any]
PlayWrightPage = Page
