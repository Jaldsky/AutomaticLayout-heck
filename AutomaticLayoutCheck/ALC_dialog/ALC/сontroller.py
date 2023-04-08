from os import path, getcwd, scandir
from pyunpack import Archive
import logging
from ALC_dialog.ALC.selenium_helper import SeleniumHelper
from ALC_dialog.ALC.image_helper import ImageHelper
from typing import List, Union, Tuple

CHROME_DRIVER_PATH = path.join(getcwd(), 'drivers', 'chromedriver.exe')
SAVE_PATH = path.join(getcwd(), 'pics')
SITE_COMPONENTS_PATH = f"file:///{path.join(getcwd(), 'data', 'site_example', 'index.html')}"

POSSIBLE_ARCHIVE_FORMATS = ['zip', 'rar']
POSSIBLE_PIC_FORMATS = ['psd']

logger = logging.getLogger(__name__)


class Controller(object):

    def __init__(self, files_data, folder_path: str):
        self.files_data = files_data
        self.folder_path = folder_path

    @staticmethod
    def unzip(site_path: str) -> List:
        file_name = str(site_path).split('\\')[-1]
        save_path = str(site_path).replace(file_name, '')
        Archive(site_path).extractall(save_path)

        folders_paths = [path.join(save_path, item.name) for item in scandir(save_path) if not item.is_file()]
        return folders_paths

    @property
    def get_site_pic_paths(self) -> Tuple[str, str]:
        site_path = str()
        sample_pic_path = str()

        if len(self.files_data) == 2:
            for elm in self.files_data:
                if elm.get('file_extension') in POSSIBLE_ARCHIVE_FORMATS:
                    site_path = elm.get('file_path')
                elif elm.get('file_extension') in POSSIBLE_PIC_FORMATS:
                    sample_pic_path = elm.get('file_path')

            if site_path == '' or sample_pic_path == '':
                logger.error('Error uploading files, please make sure you are uploading the correct format')

            return site_path, sample_pic_path
        else:
            logger.error('Added more than two files')

    def exec(self):
        site_path, sample_pic_path = self.get_site_pic_paths

        image_helper = ImageHelper()
        reference_sample = image_helper.convert_psd_to_png(sample_pic_path, self.folder_path)
        img_width, img_height = image_helper.get_image_resolution(reference_sample)

        folders_paths = self.unzip(site_path)

        # придумать что делать с разрешением изображением сайта
        # x = SeleniumHelper(SITE_COMPONENTS_PATH,
        #                    SAVE_PATH,
        #                    CHROME_DRIVER_PATH).get_full_screenshot_page


