from os import path, getcwd
from PIL import Image
from psd_tools import PSDImage


class ImageHelper(object):
    """Класс для конвертации формата изображений"""

    PIC_NAME = 'reference_sample.png'

    def convert_psd_to_png(self, path_to_pic: str, path_to_save: str) -> str:
        """Конвертация формата psd в png.

        Args:
            path_to_pic: путь до изображения.
            path_to_save: путь для сохранения.

        Returns:
            Путь с сохраненным сконвертированным изображением.
        """
        psd_pic = PSDImage.open(path_to_pic)
        save_path = path.join(path_to_save, self.PIC_NAME)
        psd_pic.composite().save(save_path)
        return save_path

    @staticmethod
    def get_image_resolution(path_to_pic):
        with Image.open(path_to_pic) as img:
            return img.size
