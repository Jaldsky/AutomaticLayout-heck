from os import path, getcwd, scandir, pardir, listdir, unlink, rename
from pyunpack import Archive
import logging
from ALC_dialog.ALC.selenium_helper import SeleniumHelper
from ALC_dialog.ALC.image_helper import ImageHelper, PIC_NAME
from typing import List, Union, Tuple
from shutil import copy
from ALC_dialog.ALC.comparator import ComparatorMeanSquaredError, ComparatorStructuralSimilarityIndex, ComparatorNeuralNetworkVGG16


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
    def rename_file(old_name, new_name):
        try:
            rename(old_name, new_name)
            logger.error(f"{old_name} has been renamed to {new_name}")
        except OSError as e:
            logger.error(f"Error: {e}")

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

        reference_sample_path = path.join(self.DISPLAY_IMAGES_PATH, PIC_NAME)
        data = {'reference_sample': reference_sample_path}
        sample_data_list = list()
        for num, site_folder_path in enumerate(site_folders_paths):  # there can be several sites in the archive
            sample_dict = dict()

            index_path = path.join(site_folder_path, 'index.html')
            sample_path = SeleniumHelper(img_width, img_height).get_full_screenshot_page(index_path, folder_path)
            self.copy_file(sample_path, self.DISPLAY_IMAGES_PATH)

            current_file_path = path.join(self.DISPLAY_IMAGES_PATH, 'sample.png')
            new_file_nam1e = f'sample_{num}.png'
            new_file_path = path.join(self.DISPLAY_IMAGES_PATH, new_file_nam1e)
            self.rename_file(current_file_path, new_file_path)

            sample_dict['name'] = new_file_nam1e
            sample_dict['path'] = new_file_path

            cmse = ComparatorMeanSquaredError(reference_sample_path, new_file_path)
            cssim = ComparatorStructuralSimilarityIndex(reference_sample_path, new_file_path)
            vgg16 = ComparatorNeuralNetworkVGG16(reference_sample_path, new_file_path)

            cmse_sim_per = round(cmse.get_similarity_percentages, 2)
            cssim_sim_per = round(cssim.get_similarity_percentages, 2)
            vgg16_sim_per = round(vgg16.get_similarity_percentages, 2)

            cmse_sim_index = round(cmse.get_similarity_index, 2)
            cssim_sim_index = round(cssim.get_similarity_index, 2)
            vgg16_sim_index = round(vgg16.get_similarity_index, 2)

            cmse_are_sim = cmse.are_images_similar
            cssim_are_sim = cssim.are_images_similar
            vgg16_are_sim = vgg16.are_images_similar

            cmse_threshold = cmse.get_threshold
            cssim_threshold = cssim.get_threshold
            vgg16_threshold = vgg16.get_threshold

            sample_dict['CMSE'] = {'index': cmse_sim_index, 'similarity_percentage': cmse_sim_per,
                                   'are_similar': cmse_are_sim, 'threshold': cmse_threshold}
            sample_dict['CSSIM'] = {'index': cssim_sim_index, 'similarity_percentage': cssim_sim_per,
                                    'are_similar': cssim_are_sim, 'threshold': cssim_threshold}
            sample_dict['VGG16'] = {'index': vgg16_sim_index, 'similarity_percentage': vgg16_sim_per,
                                    'are_similar': vgg16_are_sim, 'threshold': vgg16_threshold}
            sample_data_list.append(sample_dict)
        data['sample'] = sample_data_list

        print(data)
        return data
