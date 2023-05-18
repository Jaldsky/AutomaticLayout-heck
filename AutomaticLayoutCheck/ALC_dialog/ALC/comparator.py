from typing import Tuple, Optional
from skimage.metrics import structural_similarity
from cv2 import imread, resize, cvtColor, cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from functools import cached_property
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

    @property
    def get_threshold(self) -> float:
        """Получить порог сравнения схожести двух изображений.

        Returns:
            Порог схожести двух изображений."""
        return self.threshold

    def prepare_image(self, img_path: str, img_size: Tuple[int, int], convert_grayscale: bool = True) -> np.ndarray:
        """Подготовить изображение для сравнения: представить изображение в виде массива,
        изменить размер изображения, перевести в градации серого.

        Args:
            img_path: путь до изображения.
            img_size: размер изображения.
            convert_grayscale: перевести цветное изображение в градации серого.

        Returns:
            Обработанное изображение.
        """
        # Read a color image and represent it as an array
        img = self.imread_image(img_path)

        # Present images in the same size
        img = self.resize_image(img, img_size)

        if convert_grayscale:
            # Convert the images to grayscale
            img = self.convert_image_to_grayscale(img)
        return img


class ComparatorMeanSquaredError(ComparatorBase):
    """Класс для сравнения схожести двух изображений по методу среднеквадратичной ошибки (Mean Squared Error - MSE)."""

    def __init__(self, reference_img_path: str, sample_img_path: str, img_size: Tuple = (500, 500),
                 threshold: float = 60) -> None:
        """Инициализация класса.

        Args:
            reference_img_path: путь до эталонного изображения.
            sample_img_path: путь до сравниваемого изображения.
            img_size: размер изображения.
            threshold: попрог определения схожести изображений.
        """
        super().__init__()
        self.reference_img_path = reference_img_path
        self.sample_img_path = sample_img_path
        self.img_size = img_size
        self.threshold = threshold

    @property
    def are_images_similar(self) -> str:
        """Функция проверки схожести изображений.

        Returns:
            True - похожи, False - не похожи.
        """
        nrmse = self.compare_exec
        if nrmse >= self.threshold:
            return 'Нет'
        else:
            return 'Да'

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

    @cached_property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в индексе.
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
    def are_images_similar(self) -> str:
        """Функция проверки схожести изображений.

        Returns:
            Да - похожи, Нет - не похожи.
        """
        nrmse = self.compare_exec
        if nrmse <= self.threshold:
            return 'Нет'
        else:
            return 'Да'

    @property
    def get_similarity_percentages(self) -> float:
        """Получить процент схожести изображений.

        Returns:
            Процент схожести.
        """
        ssim = self.compare_exec
        similarity_percentage = (ssim + 1) * 50
        return similarity_percentage

    @cached_property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в индексе.
        """
        reference_img = self.prepare_image(self.reference_img_path, self.img_size)
        sample_img = self.prepare_image(self.sample_img_path, self.img_size)

        # Calculate the SSIM score
        ssim_score = structural_similarity(reference_img, sample_img)
        return ssim_score


class ComparatorNeuralNetworkVGG16(ComparatorBase):
    """Класс для сравнения схожести двух изображений на основе нейросети VGG16."""

    def __init__(self, reference_img_path: str, sample_img_path: str, img_size: Tuple = (224, 224),
                 threshold: float = 0.85) -> None:
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
    def are_images_similar(self) -> str:
        """Функция проверки схожести изображений.

        Returns:
            True - похожи, False - не похожи.
        """
        nrmse = self.compare_exec
        if nrmse <= self.threshold:
            return 'Нет'
        else:
            return 'Да'

    @property
    def get_similarity_percentages(self) -> float:
        """Получить процент схожести изображений.

        Returns:
            Процент схожести.
        """
        sim = self.compare_exec
        similarity_percentage = sim * 100
        return similarity_percentage

    @cached_property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в индексе.
        """
        reference_img = self.prepare_image(self.reference_img_path, self.img_size, convert_grayscale=False)
        sample_img = self.prepare_image(self.sample_img_path, self.img_size, convert_grayscale=False)

        # Load pre-trained CNN
        cnn = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        # Expand dimensions to match input shape of CNN
        x1 = np.expand_dims(reference_img, axis=0)
        x2 = np.expand_dims(sample_img, axis=0)

        # Normalize pixel values
        x1 = preprocess_input(x1)
        x2 = preprocess_input(x2)

        # Extract features from images using CNN
        features1 = cnn.predict(x1)
        features2 = cnn.predict(x2)

        # Compute cosine similarity between features
        vgg16 = cosine_similarity(features1.reshape(1, -1), features2.reshape(1, -1))[0][0]
        return vgg16
