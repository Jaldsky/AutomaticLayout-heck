from unittest import TestCase
from os import path, getcwd, remove

from app.engine.image_helper import (
    ImageHelper,
    ImageHelperTypeException,
    ImageHelperFileExtensionException,
    ImageHelperPSDPathHException,
    ImageHelperGetImagePathException,
)


class TestImageHelper(TestCase):
    test_data_path = path.join(getcwd(), 'app', 'tests', 'test_data')

    def test_convert_psd_to_image(self):
        psd_path = path.join(self.test_data_path, 'template_test.psd')
        save_image_path = path.join(self.test_data_path, 'site_template_test.png')

        with self.subTest('Incorrect psd_path type'):
            with self.assertRaises(ImageHelperTypeException):
                ImageHelper.convert_psd_to_image(None, save_image_path)

        with self.subTest('Incorrect save_image_path type'):
            with self.assertRaises(ImageHelperFileExtensionException):
                ImageHelper.convert_psd_to_image(psd_path, None)

        with self.subTest('Incorrect psd_path type'):
            with self.assertRaises(ImageHelperPSDPathHException):
                ImageHelper.convert_psd_to_image(self.test_data_path, save_image_path)

        with self.subTest('Convert psd file to image'):
            ImageHelper.convert_psd_to_image(psd_path, save_image_path)

            self.assertTrue(path.exists(save_image_path))
            self.assertEqual(5506, path.getsize(save_image_path))  # checking the count of bytes

            remove(save_image_path)

    def test_get_image_resolution(self):
        test_image_path = path.join(self.test_data_path, 'img_with_text_test.png')

        with self.subTest('Unknown image path'):
            with self.assertRaises(ImageHelperGetImagePathException):
                ImageHelper().get_image_resolution('test')

        with self.subTest('Unknown image path, empty str'):
            with self.assertRaises(ImageHelperGetImagePathException):
                ImageHelper().get_image_resolution('')

        with self.subTest('Get image resolution'):
            self.assertEqual((601, 639), ImageHelper().get_image_resolution(test_image_path))

    def test_read_image(self):
        test_image_path = path.join(self.test_data_path, 'img_with_text_test.png')

        with self.subTest('Read image'):
            self.assertTupleEqual((639, 601, 3), ImageHelper.read_image(test_image_path).shape)

        with self.subTest('Unknown image path'):
            with self.assertRaises(ImageHelperGetImagePathException):
                ImageHelper.read_image('')

    def test_hide_text(self):
        test_image_path = path.join(self.test_data_path, 'img_with_text_test.png')
        save_image_path = path.join(self.test_data_path, 'img_with_filled_text.png')

        with self.subTest('Hide text at image'):
            # TODO write tests for determining image shading
            ImageHelper().hide_text(test_image_path, save_image_path)
            self.assertTrue(path.exists(save_image_path))

            remove(save_image_path)
