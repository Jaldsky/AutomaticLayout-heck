from typing import Tuple
from os import path

from PIL import Image
from psd_tools import PSDImage


PIC_NAME = 'reference_sample.png'


class ImageHelper(object):
    """Класс для работы с изображениями"""

    def convert_psd_to_png(self, path_to_img: str, path_to_save: str) -> str:
        """Конвертация формата psd в png.

        Args:
            path_to_img: путь до изображения.
            path_to_save: путь для сохранения.

        Returns:
            Путь с сохраненным сконвертированным изображением.
        """
        psd_pic = PSDImage.open(path_to_img)
        save_path = path.join(path_to_save, PIC_NAME)
        psd_pic.composite().save(save_path)
        return save_path

    @staticmethod
    def get_image_resolution(path_to_img: str) -> Tuple[int, int]:
        """Функция получения разрешения изображения.

        Args:
            path_to_img: путь до изображения.

        Returns:
            Кортеж со значением ширины и высоты.
        """
        with Image.open(path_to_img) as img:
            return img.size
