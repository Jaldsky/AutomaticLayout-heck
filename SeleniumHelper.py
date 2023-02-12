from selenium import webdriver
from time import sleep
from os import path, getcwd


class SeleniumHelper(object):

    def __init__(self, browser_driver='Chrome'):
        if browser_driver.lower() == 'firefox':
            driver = webdriver.Firefox()
        elif browser_driver.lower() == 'safari':
            driver = webdriver.Safari()
        elif browser_driver.lower() == 'edge':
            driver = webdriver.Edge()
        else:
            driver = webdriver.Chrome()
        self.driver = driver

    def get_screenshot_page(self):
        file_path = f"file:///{path.join(getcwd(), 'data', 'site_example', 'index.html')}"
        self.driver.get(file_path)
        # self.driver.save_full_page_screenshot('1.png')
        sleep(5)



SeleniumHelper().get_screenshot_page()
