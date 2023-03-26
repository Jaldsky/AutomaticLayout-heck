from os import path, getcwd
from pyunpack import Archive

from ALC_dialog.ALC.selenium_helper import SeleniumHelper
from ALC_dialog.ALC.pic_format_converter import PicFormatConverter


CHROME_DRIVER_PATH = path.join(getcwd(), 'drivers', 'chromedriver.exe')
SAVE_PATH = path.join(getcwd(), 'pics')
SITE_COMPONENTS_PATH = f"file:///{path.join(getcwd(), 'data', 'site_example', 'index.html')}"


class ALC(object):

    def __init__(self, site_archive, reference_sample):
        self.site_archive = site_archive
        self.reference_sample = reference_sample
        print(site_archive)
        print(reference_sample)

    @staticmethod
    def unzip(site_archive):
        Archive(site_archive).extractall(path.join(getcwd(), 'ALC_dialog', 'ALC', 'data'))

    def exec(self):
        self.unzip(self.site_archive)
        x = SeleniumHelper(SITE_COMPONENTS_PATH,
                           SAVE_PATH,
                           CHROME_DRIVER_PATH).get_full_screenshot_page


