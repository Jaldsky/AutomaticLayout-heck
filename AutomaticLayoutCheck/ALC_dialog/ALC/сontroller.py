from os import path, getcwd, scandir, pardir, listdir, unlink
from pyunpack import Archive
import logging
from ALC_dialog.ALC.selenium_helper import SeleniumHelper
from ALC_dialog.ALC.image_helper import ImageHelper, PIC_NAME
from typing import List, Union, Tuple
from shutil import copy


POSSIBLE_ARCHIVE_FORMATS = ['zip', 'rar']
POSSIBLE_PIC_FORMATS = ['psd']

logger = logging.getLogger(__name__)


class Controller(object):
    DISPLAY_IMAGES_PATH = path.join(getcwd(), 'ALC_dialog', 'static', 'imgs')

    @staticmethod
    def unzip(site_path: str) -> List:
        file_name = str(site_path).split('\\')[-1]
        save_path = str(site_path).replace(file_name, '')
        Archive(site_path).extractall(save_path)
        folders_paths = [path.join(save_path, item.name) for item in scandir(save_path) if not item.is_file()]
        return folders_paths

    @staticmethod
    def delete_all_files_in_directory(dir_path: str) -> None:
        for file in listdir(dir_path):
            file_path = path.join(dir_path, file)
            try:
                if path.isfile(file_path):
                    unlink(file_path)
            except Exception as e:
                logger.error(f"Error deleting file {file_path}: {e}")

    @staticmethod
    def copy_file(source_path: str, dest_path: str) -> None:
        try:
            copy(source_path, dest_path)
            logger.error(f"{source_path} was copied to {dest_path} successfully")
        except FileNotFoundError:
            logger.error(f"Error: {source_path} does not exist")
        except Exception as e:
            logger.error("Error: Failed to copy file - %s", e.args)

    @staticmethod
    def get_site_pic_paths(files_data) -> Tuple[str, str]:
        site_path = str()
        sample_pic_path = str()

        if len(files_data) == 2:
            for elm in files_data:
                if elm.get('file_extension') in POSSIBLE_ARCHIVE_FORMATS:
                    site_path = elm.get('file_path')
                elif elm.get('file_extension') in POSSIBLE_PIC_FORMATS:
                    sample_pic_path = elm.get('file_path')

            if site_path == '' or sample_pic_path == '':
                logger.error('Error uploading files, please make sure you are uploading the correct format')

            return site_path, sample_pic_path
        else:
            logger.error('Added more than two files')

    def exec(self, files_data, folder_path: str):
        site_path, sample_pic_path = self.get_site_pic_paths(files_data)

        image_helper = ImageHelper()
        reference_sample = image_helper.convert_psd_to_png(sample_pic_path, folder_path)
        img_width, img_height = image_helper.get_image_resolution(reference_sample)

        site_folders_paths = self.unzip(site_path)

        self.delete_all_files_in_directory(self.DISPLAY_IMAGES_PATH)
        self.copy_file(reference_sample, self.DISPLAY_IMAGES_PATH)

        imgs_path = [path.join(self.DISPLAY_IMAGES_PATH, PIC_NAME)]
        for num, site_folder_path in enumerate(site_folders_paths):  # there can be several sites in the archive
            index_path = path.join(site_folder_path, 'index.html')
            sample_path = SeleniumHelper(img_width, img_height).get_full_screenshot_page(index_path, folder_path)
            self.copy_file(sample_path, self.DISPLAY_IMAGES_PATH)
            imgs_path.append(path.join(self.DISPLAY_IMAGES_PATH, f'{sample_path}_{num}'))
        return imgs_path
