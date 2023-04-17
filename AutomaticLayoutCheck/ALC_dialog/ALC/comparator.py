from typing import Tuple
from skimage.metrics import structural_similarity
from cv2 import imread, resize, cvtColor, cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY
import numpy as np


class ComparatorBase:
    """Базовый класс для сравнения схожести двух изображений."""

    @staticmethod
    def imread_image(img_path: str) -> np.ndarray:
        """Считать изображение.

        Args:
            img_path: путь до изображения.

        Returns:
            Данные изображения в виде массива NumPy в формате RGB.
        """
        img = imread(img_path)
        return cvtColor(img, COLOR_BGR2RGB)

    def resize_image(self, img_array: np.ndarray, size: Tuple[int, int]):
        """Изменить размер изображения.

        Args:
            img_array: изображение в виде массива.
            size: размер изображения.

        Returns:
            Изображение в виде массива с измененным размером.
        """
        return resize(img_array, size)

    def compare_exec(self, *args):
        """Выполнить сравнение схожести двух изображений."""
        pass

    def are_images_similar(self):
        """Похожи ли два изображения."""
        pass

    def get_similarity_percentages(self):
        """Получить процент схожести изображений."""
        pass


class ComparatorMeanSquaredError(ComparatorBase):
    """Класс для сравнения схожести двух изображений по методу среднеквадратичной ошибки (Mean Squared Error - MSE)."""

    def __init__(self, reference_img_path: str, sample_img_path: str, threshold: float = 96.25) -> None:
        """Инициализация класса.

        Args:
            reference_img_path: путь до эталонного изображения.
            sample_img_path: путь до сравниваемого изображения.
            threshold: попрог определения схожести изображений.
        """
        self.reference_img_path = reference_img_path
        self.sample_img_path = sample_img_path
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
        return self.compare_exec

    @property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в процентах.
        """
        reference_img = self.imread_image(self.reference_img_path)
        sample_img = self.imread_image(self.sample_img_path)

        img_size = (500, 500)

        reference_img = self.resize_image(reference_img, img_size)
        sample_img = self.resize_image(sample_img, img_size)

        # calculate the root mean square error (RMSE)
        mse = np.mean((reference_img - sample_img) ** 2)
        rmse = np.sqrt(mse)

        # calculate the maximum pixel value of the images
        max_pixel_val = np.iinfo(reference_img.dtype).max

        # calculate the normalized root mean square error (NRMSE)
        nrmse = (rmse / max_pixel_val) * 100
        return 100 - nrmse


class ComparatorStructuralSimilarityIndex(ComparatorBase):
    """Класс для сравнения схожести двух изображений по методу
    индексу структурного подобия (Structural Similarity Index - SSIM)."""

    def __init__(self, reference_img_path: str, sample_img_path: str, threshold: float = 53.5) -> None:
        """Инициализация класса.

        Args:
            reference_img_path: путь до эталонного изображения.
            sample_img_path: путь до сравниваемого изображения.
            threshold: попрог определения схожести изображений.
        """
        self.reference_img_path = reference_img_path
        self.sample_img_path = sample_img_path
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
        return self.compare_exec

    @property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в процентах.
        """
        reference_img = self.imread_image(self.reference_img_path)
        sample_img = self.imread_image(self.sample_img_path)

        img_size = (500, 500)

        reference_img = self.resize_image(reference_img, img_size)
        sample_img = self.resize_image(sample_img, img_size)

        # Convert the images to grayscale
        gray_reference_img = cvtColor(reference_img, COLOR_BGR2GRAY)
        gray_sample_img = cvtColor(sample_img, COLOR_BGR2GRAY)

        # Calculate the SSIM score
        ssim_score = structural_similarity(gray_reference_img, gray_sample_img)
        return ssim_score * 100
