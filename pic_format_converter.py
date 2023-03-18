from os import path, getcwd

from psd_tools import PSDImage


class PicFormatConverter(object):
    """Класс для конвертации формата изображений"""

    PIC_PATH = path.join(getcwd(), 'data', 'template_example.psd')
    PIC_NAME = 'reference_sample.png'

    def convert_psd_to_png(self):
        """Конвертация формата psd в png.

        Returns:
            Путь с сохраненным сконвертированным изображением.
        """
        psd_pic = PSDImage.open(self.PIC_PATH)
        return psd_pic.composite().save(path.join(getcwd(), 'pics', self.PIC_NAME))
