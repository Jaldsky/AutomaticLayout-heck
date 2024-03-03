from unittest import TestCase
from os import path, getcwd
from shutil import rmtree

from app.engine.util import unzip, UnZipFileException


class UtilTest(TestCase):

    def test_unzip(self):
        test_archive_path = path.join(getcwd(), 'app', 'tests', 'test_data', 'page_test.zip')

        with self.subTest('Unzip file'):
            unzip(test_archive_path)
            folder = path.splitext(test_archive_path)[0]
            self.assertTrue(path.exists(folder))

            rmtree(folder)

        with self.subTest('Custom save path'):
            save_path = path.join(getcwd(), 'app', 'tests', 'test_data', 'test')
            unzip(test_archive_path, save_path)
            self.assertTrue(path.exists(save_path))

            rmtree(save_path)

        with self.subTest('Unsupported type'):
            with self.assertRaises(UnZipFileException):
                unzip(test_archive_path.replace('.zip', '.7z'))
