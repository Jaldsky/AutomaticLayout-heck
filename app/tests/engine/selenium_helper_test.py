from unittest import TestCase

from app.engine.selenium_manager import SeleniumOptions, SeleniumDriver, SeleniumManager


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
        driver = SeleniumDriver()
        driver.driver.get('https://www.google.com/')
        self.assertEqual('https://www.google.com/', driver.driver.current_url)

    def test_get_full_screenshot_page(self):
        manager = SeleniumManager()
        pass
