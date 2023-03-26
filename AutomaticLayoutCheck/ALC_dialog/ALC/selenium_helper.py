from os import path, getcwd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Screenshot import Screenshot_Clipping


class SeleniumHelper(object):
    """Класс для работы с Selenium"""

    SITE_SCREENSHOT_NAME = 'sample.png'

    def __init__(self, components_path: str, save_path: str, driver_path: str):
        "добавить доку"
        self.components_path = components_path
        self.save_path = save_path
        self.driver_path = driver_path

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')

        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        self.driver = driver

    @property
    def get_full_screenshot_page(self) -> str:
        """Получение скриншота полностью всей страницы.

        Returns:
            Путь с сохраненным скриншотом.
        """
        self.driver.get(self.components_path)
        return Screenshot_Clipping.Screenshot().full_Screenshot(driver=self.driver,
                                                                save_path=self.save_path,
                                                                image_name=self.SITE_SCREENSHOT_NAME)
