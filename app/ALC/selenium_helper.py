from os import path, getcwd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Screenshot import Screenshot_Clipping


CHROME_DRIVER_PATH = path.join(getcwd(), 'drivers', 'chromedriver.exe')
SITE_SCREENSHOT_NAME = 'sample.png'


class SeleniumHelper(object):
    """Класс для работы с Selenium"""

    def __init__(self, browser_width: int = None, browser_height: int = None) -> None:
        """Инициализация класса.

        Args:
            browser_width: ширина окна браузера.
            browser_height: высота окна браузера.
        """
        self.driver_path = CHROME_DRIVER_PATH

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        if browser_width is not None or browser_height is not None:
            options.add_argument(f'--window-size={browser_width},{browser_height}')

        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        self.driver = driver

    def get_full_screenshot_page(self, index_path: str, save_img_path: str) -> str:
        """Получение скриншота всей страницы.

        Args:
            index_path: путь до изображения.
            save_img_path: путь для сохранения.

        Returns:
            Путь с сохраненным скриншотом.
        """
        self.driver.get(index_path)
        return Screenshot_Clipping.Screenshot().full_Screenshot(driver=self.driver,
                                                                save_path=save_img_path,
                                                                image_name=SITE_SCREENSHOT_NAME)
