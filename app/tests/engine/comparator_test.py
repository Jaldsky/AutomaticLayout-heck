from unittest import TestCase
from os import path, getcwd, environ

from app.engine.comparator import (
    ComparatorBase,
    ComparatorMeanSquaredError,
    ComparatorStructuralSimilarityIndex,
    ComparatorNeuralNetworkVGG16
)


class MockComparatorBase(ComparatorBase):

    def __init__(self):
        self.similarity_threshold = 0

    def compare_exec(self):
        pass


class TestCompareImages(TestCase):
    test_data_path = path.join(getcwd(), 'app', 'tests', 'test_data')

    test_reference_image_path = path.join(test_data_path, 'img_page_test.png')
    test_image_path = path.join(test_data_path, 'img_with_text_test.png')

    def test_prepare_comparison_image(self):
        test_image_path = path.join(self.test_data_path, 'img_page_test.png')
        # TODO Add test BGR to RGB

        with self.subTest('Prepare comparison image without discoloration'):
            image = MockComparatorBase().prepare_comparison_image(test_image_path, (200, 200), convert_grayscale=False)

            self.assertTupleEqual((200, 200, 3), image.shape)
            self.assertEqual(120000, image.size)

        with self.subTest('Prepare comparison image with discoloration'):
            image = MockComparatorBase().prepare_comparison_image(test_image_path, (200, 200), convert_grayscale=True)

            self.assertTupleEqual((200, 200), image.shape)
            self.assertEqual(40000, image.size)

    def test_compare_by_mean_squared_error(self):
        with self.subTest('Different images'):
            comparator = ComparatorMeanSquaredError(self.test_reference_image_path,
                                                    self.test_image_path)
            index = comparator.compare_exec()

            self.assertEqual(0.19311424, index)
            self.assertEqual(19.31, comparator.get_similarity_percentages(index))
            self.assertFalse(comparator.are_images_similar(index))

        with self.subTest('Identical images'):
            comparator = ComparatorMeanSquaredError(self.test_reference_image_path,
                                                    self.test_reference_image_path)
            index = comparator.compare_exec()

            self.assertEqual(1.0, index)
            self.assertEqual(100.00, comparator.get_similarity_percentages(index))
            self.assertTrue(comparator.are_images_similar(index))

    def test_compare_by_structural_similarity_index(self):
        with self.subTest('Different images'):
            comparator = ComparatorStructuralSimilarityIndex(self.test_reference_image_path,
                                                             self.test_image_path)
            index = comparator.compare_exec()

            self.assertEqual(0.3037992229686996, index)
            self.assertEqual(30.38, comparator.get_similarity_percentages(index))
            self.assertFalse(comparator.are_images_similar(index))

        with self.subTest('Identical images'):
            comparator = ComparatorStructuralSimilarityIndex(self.test_reference_image_path,
                                                             self.test_reference_image_path)
            index = comparator.compare_exec()

            self.assertEqual(1.0, index)
            self.assertEqual(100.00, comparator.get_similarity_percentages(index))
            self.assertTrue(comparator.are_images_similar(index))

    def test_compare_by_neural_network_vgg16(self):
        with self.subTest('Different images'):
            comparator = ComparatorNeuralNetworkVGG16(self.test_reference_image_path,
                                                      self.test_image_path)
            index = comparator.compare_exec()

            # You may see slightly different numerical results due to floating-point round-off errors from different
            # computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`
            environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
            self.assertTrue(0.37 <= comparator.get_similarity_percentages(index) >= 0.41)
            self.assertFalse(comparator.are_images_similar(index))

        with self.subTest('Identical images'):
            comparator = ComparatorNeuralNetworkVGG16(self.test_reference_image_path,
                                                      self.test_reference_image_path)
            index = comparator.compare_exec()

            self.assertEqual(1, int(index))
            self.assertEqual(100.0, comparator.get_similarity_percentages(index))
            self.assertTrue(comparator.are_images_similar(index))
