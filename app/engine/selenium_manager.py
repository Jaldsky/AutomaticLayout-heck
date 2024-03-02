from abc import ABC, abstractmethod
from os import path, getcwd
from dataclasses import dataclass, field
from typing import Optional

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome

from Screenshot import Screenshot_Clipping


CHROME_DRIVER_PATH = path.join(getcwd(), 'app', 'engine', 'drivers', 'chromedriver.exe')
SITE_SCREENSHOT_NAME = 'sample.png'


@dataclass
class SeleniumOptionsBase(ABC):
    """Base class for interacting with Selenium driver options."""
    selenium_option: Options = None

    def __post_init__(self) -> None:
        """Post initialization."""
        self.selenium_option = Options()

    @property
    @abstractmethod
    def settings(self) -> Options:
        """Property for getting the instance of the browser settings class."""
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

        driver_settings: list = self.default_settings
        if custom_settings := self.custom_settings:
            driver_settings += custom_settings

        _ = [self.selenium_option.add_argument(i) for i in set(driver_settings)]

    @property
    def settings(self) -> Options:
        """Property for getting the instance of the browser settings class.

        Returns:
            An instance of the browser settings class with the settings applied.
        """
        return self.selenium_option


@dataclass
class SeleniumDriverBase(ABC):
    """Base class for interacting with Selenium driver."""
    selenium_driver_type: str = 'Chrome'

    @property
    @abstractmethod
    def driver(self):
        """Property for getting the instance of the Selenium driver."""
        pass


@dataclass
class SeleniumDriver(SeleniumDriverBase):
    """Class for interacting with Selenium driver."""
    custom_settings: Optional[list] = None
    selenium_driver: Optional[WebDriver] = None
    driver_path: str = CHROME_DRIVER_PATH

    def __post_init__(self) -> None:
        """Post initialization."""
        if self.selenium_driver_type.lower() == 'chrome':
            self.selenium_driver = Chrome(
                executable_path=self.driver_path,
                options=SeleniumOptions(custom_settings=self.custom_settings).settings
            )
            return None
        raise SeleniumDriverException

    @property
    def driver(self):
        """Property for getting the instance of the Selenium driver.

        Returns:
            An instance of the Selenium driver.
        """
        return self.selenium_driver


@dataclass
class SeleniumManagerBase(ABC):
    """Base class for interacting with Selenium."""


@dataclass
class SeleniumManager(SeleniumManagerBase):
    """Class for interacting with Selenium."""
    custom_settings: Optional[list] = None
    driver: Optional[WebDriver] = SeleniumDriver(custom_settings=custom_settings).driver

    def get_full_screenshot_page(self, page_path: str, save_image_path: str) -> str:
        """Получение скриншота всей страницы.

        Args:
            page_path: page path.
            save_image_path: save path image.

        Returns:
            Path to save the resulting image.
        """
        self.driver.get(page_path)
        return Screenshot_Clipping.Screenshot().full_Screenshot(driver=self.driver,
                                                                save_path=save_image_path,
                                                                image_name=SITE_SCREENSHOT_NAME)


class SeleniumDriverException(Exception):

    def __str__(self):
        return 'Driver not found'
