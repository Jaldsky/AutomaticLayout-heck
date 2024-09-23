from os import path, getcwd
from shutil import rmtree
from unittest import TestCase

from app.engine.selenium_manager import SeleniumOptions, SeleniumDriver, SeleniumManager
from app.engine.util import unzip


class SeleniumHelperTest(TestCase):

    @staticmethod
    def get_options_list(selenium_options: SeleniumOptions) -> list:
        selenium_options = selenium_options.settings.to_capabilities()['goog:chromeOptions']['args']
        selenium_options.sort()
        return selenium_options

    def test_selenium_options(self):
        with self.subTest('Valid default settings values'):
            options = SeleniumOptions(default_settings=['--headless', '--start-maximized'])
            self.assertListEqual(['--headless', '--start-maximized'], self.get_options_list(options))

        with self.subTest('Doubles settings values'):
            options = SeleniumOptions(default_settings=['--headless', '--headless', '--start-maximized'])
            self.assertListEqual(['--headless', '--start-maximized'], self.get_options_list(options))

        with self.subTest('Add custom setting value'):
            options = SeleniumOptions(default_settings=['--headless', '--start-maximized'],
                                      custom_settings=['--window-size=1200,720'])
            self.assertListEqual(['--headless', '--start-maximized', '--window-size=1200,720'],
                                 self.get_options_list(options))

    def test_selenium_driver(self):
        selenium_driver = SeleniumDriver(custom_settings=['--window-size=1200,720'])
        selenium_driver.driver.get('https://www.google.com/')

        self.assertEqual('https://www.google.com/', selenium_driver.driver.current_url)
        self.assertEqual(1200, selenium_driver.driver.execute_script("return document.body.offsetWidth"))

        selenium_driver.driver.quit()

    def test_get_full_screenshot_page(self):
        test_page_archive_path = path.join(getcwd(), 'app', 'tests', 'test_data', 'page_test.zip')
        unzip(test_page_archive_path)

        with self.subTest('Get full screenshot page'):
            page_folder_path = path.splitext(test_page_archive_path)[0]
            index_html_path = path.join(page_folder_path, 'index.html')
            index_html_path = f'file://{index_html_path}' if 'file://' not in index_html_path else index_html_path
            manager = SeleniumManager()

            self.assertIn(path.join(page_folder_path, 'page.png'), manager.get_full_screenshot_page(index_html_path))

            manager.driver.quit()
            rmtree(path.splitext(test_page_archive_path)[0])

        # TODO Add cases:
        # 1. index_html_path not found path
        # 2. total_width or total_height equals 0
        # 3. save_screenshot timeout error
