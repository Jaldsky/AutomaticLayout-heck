from abc import ABC, abstractmethod
from os import path, getcwd
from dataclasses import dataclass, field
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome

from Screenshot import Screenshot_Clipping


CHROME_DRIVER_PATH = path.join(getcwd(), 'app', 'engine', 'drivers', 'chromedriver.exe')
SITE_SCREENSHOT_NAME = 'sample.png'


@dataclass
class SeleniumOptionsBase(ABC):
    """Base class for interacting with Selenium driver options."""
    settings: Options = None

    def __post_init__(self) -> None:
        self.settings = Options()

    @property
    @abstractmethod
    def get_settings(self):
        pass


@dataclass
class SeleniumOptions(SeleniumOptionsBase):
    """Class for interacting with Selenium driver options."""
    custom_settings: Optional[list] = None
    default_settings: list = field(default_factory=lambda: [
        '--headless',
        '--start-maximized',
    ])

    def __post_init__(self) -> None:
        """Post initialization."""
        super().__post_init__()

        web_driver_settings: list = self.default_settings
        if custom_settings := self.custom_settings:
            web_driver_settings += custom_settings

        _ = [self.settings.add_argument(i) for i in set(web_driver_settings)]

    @property
    def get_settings(self) -> Options:
        """Method for getting an instance of the browser settings class.

        Returns:
            An instance of the browser settings class with the settings applied.
        """
        return self.settings


@dataclass
class SeleniumDriverBase(ABC):
    """Base class for interacting with Selenium driver."""
    selenium_driver_type: str = 'Chrome'


@dataclass
class SeleniumDriver(SeleniumDriverBase):
    """Class for interacting with Selenium driver."""
    custom_settings: Optional[list] = None
    driver: Optional[WebDriver] = None
    driver_path: str = CHROME_DRIVER_PATH

    def __post_init__(self) -> None:
        """Post initialization."""
        if self.selenium_driver_type.lower() == 'chrome':
            self.driver = Chrome(
                executable_path=self.driver_path,
                options=SeleniumOptions(
                    custom_settings=self.custom_settings
                ).get_settings
            )
            return None
        raise SeleniumDriverException


@dataclass
class SeleniumManagerBase(ABC):
    """Base class for interacting with Selenium."""


@dataclass
class SeleniumManager(SeleniumManagerBase):
    """Class for interacting with Selenium."""
    custom_settings: Optional[list] = None
    selenium_driver: Optional[SeleniumDriver] = None

    def __post_init__(self):
        self.selenium_driver = SeleniumDriver(custom_settings=self.custom_settings)

    def get_full_screenshot_page(self, page_path: str, save_image_path: str) -> str:
        """Получение скриншота всей страницы.

        Args:
            page_path: page path.
            save_image_path: save path image.

        Returns:
            Путь с сохраненным скриншотом.
        """
        self.driver.get(index_path)
        return Screenshot_Clipping.Screenshot().full_Screenshot(driver=self.driver,
                                                                save_path=save_img_path,
                                                                image_name=SITE_SCREENSHOT_NAME)


class SeleniumDriverException(Exception):

    def __str__(self):
        return 'Driver not found'
