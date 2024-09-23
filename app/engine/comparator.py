from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray, mean, expand_dims
from skimage.metrics import structural_similarity
from sklearn.metrics.pairwise import cosine_similarity
from keras.src.applications.vgg16 import VGG16, preprocess_input

from app.engine.image_helper import ImageHelper


@dataclass
class ComparatorInterface(ABC):
    """Interface for comparing image similarity."""
    reference_image_path: str
    image_path: str

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
    image_size: tuple[int, int]
    similarity_threshold: float
    image_helper: ImageHelper = ImageHelper()

    @abstractmethod
    def compare_exec(self, *args) -> float:
        """Method for performing image similarity comparison."""

    @staticmethod
    def get_similarity_percentages(compare_index: float, round_value: int = 2) -> float:
        """Method for obtaining the percentage of similarity between two images.

        Args:
            compare_index: image similarity index.
            round_value: rounding value.

        Returns:
            Percentage of similarity between images.
        """
        # TODO add unit test
        return round(compare_index * 100, round_value)

    def are_images_similar(self, compare_index: float) -> bool:
        """Method for obtaining an assertion of image similarity.

        Args:
            compare_index: image similarity index.

        Returns:
            Compare the images and determine if they are similar.
        """
        # TODO add unit test
        return compare_index >= self.similarity_threshold

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
        image = self.image_helper.read_image(image_path)

        image = self.image_helper.convert_image_bgr_to_rgb(image)
        image = self.image_helper.resize_image(image, image_size)

        if convert_grayscale:
            image = self.image_helper.convert_image_to_grayscale(image)
        return image


@dataclass
class ComparatorMeanSquaredError(ComparatorBase):
    """Class for comparing image similarity using the Mean Squared Error - MSE."""
    image_size: tuple[int, int] = (500, 500)
    similarity_threshold: float = 0.45

    def compare_exec(self) -> float:
        """Method for performing image similarity comparison..

        Returns:
            Image similarity index.
        """
        reference_image = self.prepare_comparison_image(self.reference_image_path, image_size=self.image_size)
        image = self.prepare_comparison_image(self.image_path, image_size=self.image_size)
        return 1 - (mean((reference_image - image) ** 2) / 100)


@dataclass
class ComparatorStructuralSimilarityIndex(ComparatorBase):
    """Class for comparing image similarity using Structural Similarity Index Measure - SSIM."""
    image_size: tuple[int, int] = (500, 500)
    similarity_threshold: float = 0.5

    def compare_exec(self) -> float:
        """Method for performing image similarity comparison..

        Returns:
            Image similarity index.
        """
        reference_image = self.prepare_comparison_image(self.reference_image_path, image_size=self.image_size)
        image = self.prepare_comparison_image(self.image_path, image_size=self.image_size)
        return structural_similarity(reference_image, image)


@dataclass
class ComparatorNeuralNetworkVGG16(ComparatorBase):
    """Class for comparing the similarity of two images based on the VGG16 neural network."""
    image_size: tuple[int, int] = (224, 224)
    similarity_threshold: float = 0.8

    def compare_exec(self) -> float:
        """Method for performing image similarity comparison..

        Returns:
            Image similarity index.
        """
        reference_image = self.prepare_comparison_image(self.reference_image_path,
                                                        image_size=self.image_size,
                                                        convert_grayscale=False)
        image = self.prepare_comparison_image(self.image_path,
                                              image_size=self.image_size,
                                              convert_grayscale=False)

        cnn = VGG16(weights='imagenet', include_top=False, input_shape=tuple([*self.image_size, 3]))

        reference_image = expand_dims(reference_image, axis=0)
        image = expand_dims(image, axis=0)

        reference_image = preprocess_input(reference_image)
        image = preprocess_input(image)

        features1 = cnn.predict(reference_image)
        features2 = cnn.predict(image)
        return cosine_similarity(features1.reshape(1, -1), features2.reshape(1, -1))[0][0]
