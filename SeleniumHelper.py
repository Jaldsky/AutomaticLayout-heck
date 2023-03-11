from os import path, getcwd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Screenshot import Screenshot_Clipping


class SeleniumHelper(object):
    """Класс для работы с Selenium"""

    CHROME_DRIVER_PATH = path.join(getcwd(), 'drivers', 'chromedriver.exe')
    SITE_COMPONENTS_PATH = f"file:///{path.join(getcwd(), 'data', 'site_example', 'index.html')}"
    SITE_SCREENSHOT_NAME = 'reference_sample.png'
    SAVE_PATH = path.join(getcwd(), 'pics')

    def __init__(self):
        """Инициализация настроек"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')

        driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_PATH, chrome_options=options)
        self.driver = driver

    def get_full_screenshot_page(self) -> str:
        """Получение скриншота полностью всей страницы.

        Returns:
            Путь с сохраненным скриншотом.
        """
        self.driver.get(self.SITE_COMPONENTS_PATH)
        return Screenshot_Clipping.Screenshot().full_Screenshot(driver=self.driver,
                                                                save_path=self.SAVE_PATH,
                                                                image_name=self.SITE_SCREENSHOT_NAME)
