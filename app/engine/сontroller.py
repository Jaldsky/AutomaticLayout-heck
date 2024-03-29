from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, Type

from app.engine.comparator import (
    ComparatorMeanSquaredError,
    ComparatorStructuralSimilarityIndex,
    ComparatorNeuralNetworkVGG16
)
from app.engine.image_helper import ImageHelper
from app.engine.selenium_manager import SeleniumManager
from app.engine.util import unzip, find_files_with_name, remove_folder_or_file, join_path
from app.models import UserSettings, Comparison, UserSession
from main.settings import CACHE_PATH, MSE_THRESHOLD, SSIM_THRESHOLD, VGG16_THRESHOLD


@dataclass
class CompareControllerBase(ABC):
    """Base class to control the execution of image similarity checks."""

    @abstractmethod
    def exec(self):
        pass


@dataclass
class CompareController(CompareControllerBase):
    """Class for controlling the execution of image similarity checks."""
    user_id: int

    def __post_init__(self):
        self.image_helper: ImageHelper = ImageHelper()
        self.selenium_manager: SeleniumManager = SeleniumManager()

    @property
    def user_session_model(self):
        return UserSession.objects.get(user_id=self.user_id)

    @property
    def user_settings_model(self):
        return UserSettings.objects.get(user_id=self.user_id)

    @property
    def user_comparison_model(self):
        return Comparison.objects.get(user_id=self.user_id)

    @property
    def cache_path_folder(self) -> str:
        return join_path([CACHE_PATH, self.user_session_model.uui])

    def get_rendered_sits_image_paths(self) -> list[str]:
        # TODO remove hardcode style: archive, index, site_image to external variable
        # TODO add exceptions + tests
        archive_path = find_files_with_name(self.cache_path_folder, 'archive', inclusion=True)[0]
        folder_path = unzip(archive_path)
        remove_folder_or_file(archive_path)

        indexes = find_files_with_name(folder_path, 'index', inclusion=True)

        images = [self.selenium_manager.get_full_screenshot_page(
            index_path, join_path([self.cache_path_folder, f'site_image_{number}.png']))
             for number, index_path in enumerate(indexes)
        ]
        remove_folder_or_file(folder_path)
        return images

    def get_reference_image_path(self):
        # TODO add exceptions + tests
        # TODO remove hardcode style: template
        template_path = find_files_with_name(self.cache_path_folder, 'template', inclusion=True)[0]
        save_image_path = join_path([self.cache_path_folder, 'reference_image.png'])
        self.image_helper.convert_psd_to_image(template_path, save_image_path)

        remove_folder_or_file(template_path)
        return save_image_path

    def compare_exec(self,
                     comparator: Type[Union['ComparatorMeanSquaredError',
                                            'ComparatorStructuralSimilarityIndex',
                                            'ComparatorNeuralNetworkVGG16']],
                     reference_image_path: str,
                     image_paths: list):
        if comparator is ComparatorMeanSquaredError:
            method, threshold = 'MSE', MSE_THRESHOLD
        elif comparator is ComparatorStructuralSimilarityIndex:
            method, threshold = 'SSIM', SSIM_THRESHOLD
        elif comparator is ComparatorNeuralNetworkVGG16:
            method, threshold = 'VGG16', VGG16_THRESHOLD
        else:
            raise Exception

        for image_path in image_paths:
            comparator = comparator(reference_image_path, image_path)
            index = comparator.compare_exec()

            Comparison.objects.create(
                user_session=self.user_session_model,
                method=method,
                threshold=threshold,
                value=index,
                percentages=comparator.get_similarity_percentages(index),
                is_similar=comparator.are_images_similar(index)
            )

    def exec(self):
        reference_image_path = self.get_reference_image_path()

        if self.user_settings_model.hide_text:
            # TODO add rewrite image method, delete old image, add new
            image = self.image_helper.read_image(reference_image_path)
            image = self.image_helper.hide_text(image)
            reference_image_path = self.image_helper.write_image(image, reference_image_path)

        image_paths = self.get_rendered_sits_image_paths()

        # TODO Add tests + catch exceptions
        if self.user_settings_model.mse:
            self.compare_exec(ComparatorMeanSquaredError, reference_image_path, image_paths)
        if self.user_settings_model.ssim:
            self.compare_exec(ComparatorStructuralSimilarityIndex, reference_image_path, image_paths)
        if self.user_settings_model.vgg16:
            self.compare_exec(ComparatorNeuralNetworkVGG16, reference_image_path, image_paths)
