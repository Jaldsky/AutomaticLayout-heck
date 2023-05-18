from typing import Dict, List, Tuple, Optional
from os import path, getcwd, scandir, listdir, unlink, rename
from shutil import copy
import logging

from pyunpack import Archive

from ALC_dialog.models import ProjectSettings

from ALC_dialog.ALC.selenium_helper import SeleniumHelper
from ALC_dialog.ALC.image_helper import ImageHelper, PIC_NAME


from ALC_dialog.ALC.comparator import ComparatorMeanSquaredError, ComparatorStructuralSimilarityIndex, \
    ComparatorNeuralNetworkVGG16


POSSIBLE_ARCHIVE_FORMATS = ['zip', 'rar']
POSSIBLE_PIC_FORMATS = ['psd']

logger = logging.getLogger(__name__)


class Controller:
    """Класс для контроля выполнения проверки схожести двух изображений."""
    display_img_path = path.join(getcwd(), 'ALC_dialog', 'static', 'imgs')

    @staticmethod
    def unzip(site_path: str) -> List:
        """Функция для распаковки архива сайта.

        Args:
            site_path: путь до архива.

        Returns:
            Список путей с указанием расположения распакованных сайтов.
        """
        file_name = str(site_path).split('\\')[-1]
        save_path = str(site_path).replace(file_name, '')
        Archive(site_path).extractall(save_path)
        folders_paths = [path.join(save_path, item.name) for item in scandir(save_path) if not item.is_file()]
        return folders_paths

    @staticmethod
    def delete_all_files_in_directory(dir_path: str) -> None:
        """Функция для удаления всех файлов в директории.

        Args:
            dir_path: путь до директории.
        """
        for file in listdir(dir_path):
            file_path = path.join(dir_path, file)
            try:
                if path.isfile(file_path):
                    unlink(file_path)
            except Exception as e:
                logger.error(f"Error deleting file {file_path}: {e}")

    @staticmethod
    def copy_file(source_path: str, dest_path: str) -> None:
        """Функция для копирования файлов.

        Args:
            source_path: путь до файла, который необходимо скопировать.
            dest_path: путь до файла для сохранения.
        """
        try:
            copy(source_path, dest_path)
            logger.error(f"{source_path} was copied to {dest_path} successfully")
        except FileNotFoundError:
            logger.error(f"Error: {source_path} does not exist")
        except Exception as e:
            logger.error("Error: Failed to copy file - %s", e.args)

    @staticmethod
    def rename_file(old_name_path: str, new_name_path: str) -> None:
        """Функция для переименования файла.

        Args:
            old_name_path: путь до файла для переименования.
            new_name_path: пусть до сохранения переименованного файла.
        """
        try:
            rename(old_name_path, new_name_path)
            logger.error(f"{old_name_path} has been renamed to {new_name_path}")
        except OSError as e:
            logger.error(f"Error: {e}")

    @staticmethod
    def get_site_img_paths(files_data: List) -> Optional[Tuple[str, str]]:
        """Функция для получения пути до эталонного изображения и архива с сайтами.

        Args:
            files_data: список с путями.

        Returns:
            Кортеж с путем до эталонного изображения и архива с сайтами.
        """
        site_path = str()
        sample_pic_path = str()

        if len(files_data) == 2:
            for elm in files_data:
                if not elm:
                    logger.error('Error uploading files, please make sure you are uploading the correct format')
                    return None
                if elm.get('file_extension') in POSSIBLE_ARCHIVE_FORMATS:
                    site_path = elm.get('file_path')
                elif elm.get('file_extension') in POSSIBLE_PIC_FORMATS:
                    sample_pic_path = elm.get('file_path')

            return site_path, sample_pic_path
        else:
            logger.error('Added more than two files')
            return None

    def exec(self, files_data: List, folder_path: str) -> Optional[Dict]:
        """Функция для выполнения основной логики класса.

        Args:
            files_data: список с путями.
            folder_path: путь до папки сохранения кеша.

        Returns:
            Словарь с парамметрами для html шаблона.
        """
        site_pic_paths = self.get_site_img_paths(files_data)
        if not site_pic_paths:
            return None

        site_path, sample_pic_path = site_pic_paths

        image_helper = ImageHelper()
        reference_sample = image_helper.convert_psd_to_png(sample_pic_path, folder_path)
        if ProjectSettings.objects.get().bedaub_text:
            reference_sample = image_helper.bedaub_text(reference_sample, reference_sample)
        img_width, img_height = image_helper.get_image_resolution(reference_sample)

        site_folders_paths = self.unzip(site_path)

        self.delete_all_files_in_directory(self.display_img_path)
        self.copy_file(reference_sample, self.display_img_path)

        reference_sample_path = path.join(self.display_img_path, PIC_NAME)
        data = {'reference_sample': reference_sample_path}
        sample_data_list = list()
        for num, site_folder_path in enumerate(site_folders_paths):  # there can be several sites in the archive
            sample_dict = dict()

            index_path = path.join(site_folder_path, 'index.html')
            sample_path = SeleniumHelper(img_width, img_height).get_full_screenshot_page(index_path, folder_path)
            self.copy_file(sample_path, self.display_img_path)

            current_file_path = path.join(self.display_img_path, 'sample.png')
            new_file_nam1e = f'sample_{num}.png'
            new_file_path = path.join(self.display_img_path, new_file_nam1e)
            self.rename_file(current_file_path, new_file_path)

            if ProjectSettings.objects.get().bedaub_text:
                new_file_path = image_helper.bedaub_text(new_file_path, new_file_path)

            sample_dict['name'] = new_file_nam1e
            sample_dict['path'] = new_file_path

            if ProjectSettings.objects.get().mse_comparator:
                cmse = ComparatorMeanSquaredError(reference_sample_path, new_file_path)
                cmse_sim_per = round(cmse.get_similarity_percentages, 2)
                cmse_sim_index = round(cmse.get_similarity_index, 2)
                cmse_are_sim = cmse.are_images_similar
                cmse_threshold = cmse.get_threshold

                sample_dict['CMSE'] = {'index': cmse_sim_index, 'similarity_percentage': cmse_sim_per,
                                       'are_similar': cmse_are_sim, 'threshold': cmse_threshold}
            if ProjectSettings.objects.get().ssim_comparator:
                cssim = ComparatorStructuralSimilarityIndex(reference_sample_path, new_file_path)
                cssim_sim_per = round(cssim.get_similarity_percentages, 2)
                cssim_sim_index = round(cssim.get_similarity_index, 2)
                cssim_are_sim = cssim.are_images_similar
                cssim_threshold = cssim.get_threshold

                sample_dict['CSSIM'] = {'index': cssim_sim_index, 'similarity_percentage': cssim_sim_per,
                                        'are_similar': cssim_are_sim, 'threshold': cssim_threshold}
            if ProjectSettings.objects.get().vgg16_comparator:
                cvgg16 = ComparatorNeuralNetworkVGG16(reference_sample_path, new_file_path)
                vgg16_sim_per = round(cvgg16.get_similarity_percentages, 2)
                vgg16_sim_index = round(cvgg16.get_similarity_index, 2)
                vgg16_are_sim = cvgg16.are_images_similar
                cvgg16_threshold = cvgg16.get_threshold
                sample_dict['VGG16'] = {'index': vgg16_sim_index, 'similarity_percentage': vgg16_sim_per,
                                        'are_similar': vgg16_are_sim, 'threshold': cvgg16_threshold}

            sample_data_list.append(sample_dict)
        data['sample'] = sample_data_list
        return data
