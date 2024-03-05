from unittest import TestCase
from os import path, getcwd

from app.engine.comparator import ComparatorBase


class TestPrepareComparisonImage(TestCase):
    test_data_path = path.join(getcwd(), 'app', 'tests', 'test_data')

    def test_prepare_comparison_image(self):
        test_image_path = path.join(self.test_data_path, 'img_with_text_test.png')
        ComparatorBase(1.0).prepare_comparison_image(test_image_path, (200, 200))

