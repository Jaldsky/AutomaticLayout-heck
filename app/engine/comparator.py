from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple
from skimage.metrics import structural_similarity
import cv2
# from cv2 import imread, resize, cvtColor, cvtColor, COLOR_BGR2RGB, COLOR_BGR2GRAY
from sklearn.metrics.pairwise import cosine_similarity

from keras.applications.resnet import preprocess_input
from keras.applications.vgg16 import VGG16


# from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from functools import cached_property
from numpy import ndarray

from app.engine.image_helper import ImageHelper


@dataclass
class ComparatorInterface(ABC):
    """Interface for comparing image similarity."""

    @staticmethod
    @abstractmethod
    def get_similarity_percentages(compare_index: float) -> float:
        """Method for obtaining the percentage of similarity between two images."""

    @abstractmethod
    def are_images_similar(self, compare_index: float) -> bool:
        """Method for obtaining an assertion of image similarity."""

    @abstractmethod
    def prepare_comparison_image(self, *args):
        """Method for preparing an image for comparison."""


@dataclass
class ComparatorBase(ComparatorInterface):
    """Base class for comparing image similarity."""
    similarity_threshold: float
    image_helper: ImageHelper = ImageHelper()

    @abstractmethod
    def compare_exec(self, *args) -> float:
        """Method for performing image similarity comparison."""

    @staticmethod
    def get_similarity_percentages(compare_index: float) -> float:
        """Method for obtaining the percentage of similarity between two images.

        Args:
            compare_index: image similarity index.

        Returns:
            Percentage of similarity between images.
        """
        # TODO add unit test
        return compare_index * 100

    def are_images_similar(self, compare_index: float) -> bool:
        """Method for obtaining an assertion of image similarity.

        Args:
            compare_index: image similarity index.

        Returns:
            Compare the images and determine if they are similar.
        """
        # TODO add unit test
        return compare_index <= self.similarity_threshold

    def prepare_comparison_image(self, image_path: str,
                                 image_size: tuple[int, int],
                                 convert_grayscale: bool = True) -> ndarray:
        """Method for preparing an image for comparison.
        1. Represent the image as an array.
        2. Convert to grayscale.
        3. Normalize size.

        Args:
            image_path: path to image.
            image_size: image size.
            convert_grayscale: convert image to grayscale.

        Returns:
            Pre-processed image(pixel matrix) is ready for comparison.
        """
        # TODO add unit test
        image = self.image_helper.read_image(image_path)

        image = self.image_helper.convert_image_bgr_to_rgb(image)
        image = self.image_helper.resize_image(image, image_size)

        if convert_grayscale:
            image = self.image_helper.convert_image_to_grayscale(image)
        return image


class ComparatorMeanSquaredError(ComparatorBase):
    """Класс для сравнения схожести двух изображений по методу среднеквадратичной ошибки (Mean Squared Error - MSE)."""

    def __init__(self, reference_img_path: str, sample_img_path: str, img_size: Tuple = (500, 500),
                 threshold: float = 0.45) -> None:
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
        if nrmse <= self.threshold:
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
        similarity_percentage = mse * 100
        return similarity_percentage

    @cached_property
    def compare_exec(self) -> float:
        """Выполнить сравнение схожести двух изображений.

        Returns:
            Схожесть двух изображений в индексе.
        """
        reference_img = self.prepare_image(self.reference_img_path, self.img_size)
        sample_img = self.prepare_image(self.sample_img_path, self.img_size)

        # calculate the root mean square error (MSE)
        mse = np.mean((reference_img - sample_img) ** 2)
        return 1 - (mse / 100)


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
        similarity_percentage = ssim * 100
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
                 threshold: float = 0.8) -> None:
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
