from typing import Tuple
from skimage.metrics import structural_similarity
from cv2 import imread, resize, cvtColor, cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY
import numpy as np


class ComparatorBase:
    """Базовый класс для сравнения схожести двух изображений."""

    def __init__(self):
        self.threshold = None

    def compare_exec(self, *args):
        """Выполнить сравнение схожести двух изображений."""
        pass

    def get_similarity_percentages(self):
        """Получить процент схожести двух изображений."""
        pass

    def are_images_similar(self):
        """Функция проверки схожести изображений."""
        pass

    @staticmethod
    def imread_image(img_path: str) -> np.ndarray:
        """Считать цветное изображение.

        Args:
            img_path: путь до изображения.

        Returns:
            Данные изображения в виде массива NumPy в формате RGB.
        """
        img = imread(img_path)
        return cvtColor(img, COLOR_BGR2RGB)

    @staticmethod
    def resize_image(img_array: np.ndarray, size: Tuple[int, int]):
        """Изменить размер изображения.

        Args:
            img_array: изображение в виде массива.
            size: размер изображения.

        Returns:
            Изображение в виде массива с измененным размером.
        """
        return resize(img_array, size)

    @staticmethod
    def convert_image_to_grayscale(img_array: np.ndarray,) -> np.ndarray:
        """Перевести цветное изображение в оттенки серого.

        Args:
            img_array: изображение в виде массива.

        Returns:
            Изображение в виде массива с переведенным в градации серого цветами.
        """
        return cvtColor(img_array, COLOR_BGR2GRAY)

    @property
    def get_similarity_index(self):
        """Получить индекс схожести двух изображений.

        Returns:
            Схожесть двух изображений в процентах."""
        return self.compare_exec

    def prepare_image(self, img_path: str, img_size: Tuple[int, int]) -> np.ndarray:
        """Подготовить изображение для сравнения: представить изображение в виде массива,
        изменить размер изображения, перевести в градации серого.

        Args:
            img_path: путь до изображения.
            img_size: размер изображения.

        Returns:
            Обесцвеченное с измененным размером, представленное в виде массива изображение.
        """
        # Read a color image and represent it as an array
        img = self.imread_image(img_path)

        # Present images in the same size
        img = self.resize_image(img, img_size)

        # Convert the images to grayscale
        img = self.convert_image_to_grayscale(img)
        return img


class ComparatorMeanSquaredError(ComparatorBase):
    """Класс для сравнения схожести двух изображений по методу среднеквадратичной ошибки (Mean Squared Error - MSE)."""

    def __init__(self, reference_img_path: str, sample_img_path: str,
                 img_size: Tuple = (500, 500), threshold: float = 60) -> None:
        """Инициализация класса.

        Args:
            reference_img_path: путь до эталонного изображения.
            sample_img_path: путь до сравниваемого изображения.
            img_size: размер изображения.
            threshold: попрог определения схожести изображений.
        """
        self.reference_img_path = reference_img_path
        self.sample_img_path = sample_img_path
        self.img_size = img_size
        self.threshold = threshold

    @property
    def are_images_similar(self) -> bool:
        """Функция проверки схожести изображений.

        Returns:
            True - похожи, False - не похожи.
        """
        nrmse = self.compare_exec
        if nrmse >= self.threshold:
            return False
        else:
            return True

    @property
    def get_similarity_percentages(self) -> float:
        """Получить процент схожести двух изображений.

        Returns:
            Процент схожести двух изображений.
        """
        mse = self.compare_exec
        max_pixel_value = 255  # grayscale image
        similarity_percentage = ((max_pixel_value ** 2) - mse) / (max_pixel_value ** 2) * 100
        return similarity_percentage

    @property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в процентах.
        """
        reference_img = self.prepare_image(self.reference_img_path, self.img_size)
        sample_img = self.prepare_image(self.sample_img_path, self.img_size)

        # calculate the root mean square error (RMSE)
        mse = np.mean((reference_img - sample_img) ** 2)
        return mse


class ComparatorStructuralSimilarityIndex(ComparatorBase):
    """Класс для сравнения схожести двух изображений по методу
    индексу структурного подобия (Structural Similarity Index - SSIM)."""

    def __init__(self, reference_img_path: str, sample_img_path: str, img_size: Tuple = (500, 500),
                 threshold: float = 0.5) -> None:
        """Инициализация класса.

        Args:
            reference_img_path: путь до эталонного изображения.
            sample_img_path: путь до сравниваемого изображения.
            threshold: попрог определения схожести изображений.
        """
        super().__init__()
        self.reference_img_path = reference_img_path
        self.sample_img_path = sample_img_path
        self.img_size = img_size
        self.threshold = threshold

    @property
    def are_images_similar(self) -> bool:
        """Функция проверки схожести изображений.

        Returns:
            True - похожи, False - не похожи.
        """
        nrmse = self.compare_exec
        if nrmse <= self.threshold:
            return False
        else:
            return True

    @property
    def get_similarity_percentages(self) -> float:
        """Получить процент схожести изображений.

        Returns:
            Процент схожести.
        """
        ssim = self.compare_exec
        similarity_percentage = (ssim + 1) * 50
        return similarity_percentage

    @property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в процентах.
        """
        reference_img = self.prepare_image(self.reference_img_path, self.img_size)
        sample_img = self.prepare_image(self.sample_img_path, self.img_size)

        # Calculate the SSIM score
        ssim_score = structural_similarity(reference_img, sample_img)
        return ssim_score
