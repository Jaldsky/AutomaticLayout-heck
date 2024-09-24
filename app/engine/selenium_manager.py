from abc import ABC, abstractmethod
from os import path, getcwd
from dataclasses import dataclass, field
from typing import Optional

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome


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


class SeleniumDriverBase(ABC):
    """Base class for interacting with Selenium driver."""
    selenium_driver_type: str = 'Chrome'

    @property
    @abstractmethod
    def driver(self):
        """Property for getting the instance of the Selenium driver."""
        pass


class SeleniumDriver(SeleniumDriverBase):
    """Class for interacting with Selenium driver."""
    custom_settings: Optional[list] = None

    def __init__(self, custom_settings: Optional[list] = None) -> None:
        if self.selenium_driver_type.lower() == 'chrome':
            try:
                self.selenium_driver: WebDriver = Chrome(
                    options=SeleniumOptions(custom_settings=custom_settings).settings
                )
            except Exception:
                raise SeleniumDriverException

    @property
    def driver(self) -> WebDriver:
        """Property for getting the instance of the Selenium driver.

        Returns:
            An instance of the Selenium driver.
        """
        return self.selenium_driver


class SeleniumManagerBase(ABC):
    """Base class for interacting with Selenium."""


class SeleniumManager(SeleniumManagerBase):
    """Class for interacting with Selenium."""

    def __init__(self, custom_settings: Optional[list] = None):
        self.driver: WebDriver = SeleniumDriver(custom_settings=custom_settings).driver

    def get_full_screenshot_page(self, page_path: str, save_image_path: Optional[str] = None) -> str:
        """Получение скриншота всей страницы.

        Args:
            page_path: page path.
            save_image_path: save path image.

        Returns:
            Path to save the resulting image.
        """
        folder_save_path = path.dirname(page_path)
        if not save_image_path:
            save_image_path = path.join(folder_save_path, 'page.png')

        self.driver.get(page_path)
        total_width = self.driver.execute_script("return document.body.offsetWidth")
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(total_width, total_height)
        self.driver.save_screenshot(save_image_path)
        return save_image_path


class SeleniumDriverException(Exception):

    def __str__(self):
        return 'Driver not found'
