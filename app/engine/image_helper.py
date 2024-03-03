from abc import ABC
from enum import Enum

import cv2
import easyocr
from PIL import Image
from psd_tools import PSDImage


FILL_TEXT_COLOR = (0, 255, 0)  # green


class Language(str, Enum):
    english = 'en'
    russian = 'ru'

    def __str__(self) -> str:
        return str.__str__(self)


class ImageHelperBase(ABC):
    """Base class for interacting with images."""


class ImageHelper(ImageHelperBase):
    """Class for interacting with images."""

    @staticmethod
    def convert_psd_to_image(psd_path: str, save_image_path: str) -> None:
        """Method for converting psd to png format.

        Args:
            psd_path: path to psd file.
            save_image_path: save path image.
        """
        try:
            PSDImage.open(psd_path).composite().save(save_image_path)
        except TypeError:
            raise ImageHelperTypeException
        except ValueError:
            raise ImageHelperFileExtensionException
        except (FileNotFoundError, PermissionError):
            raise ImageHelperPSDPathHException

    @staticmethod
    def get_image_object(image_path: str):
        """Method to get an image object.

        Args:
            image_path: path to image.

        Returns:
            Image object.
        """
        try:
            with Image.open(image_path) as image:
                return image
        except (FileNotFoundError, AttributeError):
            raise ImageHelperGetImagePathException

    def get_image_resolution(self, image_path: str) -> tuple[int, int]:
        """Image resolution method.

        Args:
            image_path: path to image.

        Returns:
            Tuple with width and height values.
        """
        return self.get_image_object(image_path).size

    @staticmethod
    def hide_text(image_path: str, save_image_path: str, languages=(Language.english, Language.russian)) -> None:
        """Method to find text in an image and hide it.

        Args:
            image_path: path to image.
            save_image_path: save path image.
            languages: cortege with languages.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ImageHelperGetImagePathException

        reader = easyocr.Reader(languages)
        results = reader.readtext(image)

        for result in results:
            bbox = result[0]
            x1, y1 = int(bbox[0][0]), int(bbox[0][1])
            x2, y2 = int(bbox[2][0]), int(bbox[2][1])
            cv2.rectangle(image, (x1, y1), (x2, y2), FILL_TEXT_COLOR, cv2.FILLED)

        cv2.imwrite(save_image_path, image)


class ImageHelperTypeException(Exception):

    def __str__(self):
        return 'Incorrect type of argument passed.'


class ImageHelperFileExtensionException(Exception):

    def __str__(self):
        return 'Unknown or unspecified file extension.'


class ImageHelperPSDPathHException(Exception):

    def __str__(self):
        return 'Could not get the path to the psd file.'


class ImageHelperGetImagePathException(Exception):

    def __str__(self):
        return 'Failed to get image.'