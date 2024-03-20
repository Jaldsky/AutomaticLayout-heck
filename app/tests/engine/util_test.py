from unittest import TestCase
from os import path, getcwd, makedirs
from shutil import rmtree
from random import choices
from string import ascii_lowercase


from app.engine.util import (
    unzip,
    search_folder_key_file_paths,
    InvalidArchivePathException,
    ArchivePathNotFoundException,
    UnsupportedArchiveFormatException
)


class UtilTest(TestCase):
    test_data = path.join(getcwd(), 'app', 'tests', 'test_data')

    @staticmethod
    def create_pages_structure(root_dir: str, key_file: str, count_pages: int):
        makedirs(root_dir)
        for _ in range(count_pages):
            subdir_name = ''.join(choices(ascii_lowercase, k=5))
            subdir_path = path.join(root_dir, subdir_name)
            makedirs(subdir_path)
            with open(path.join(root_dir, subdir_path, key_file), 'w') as file:
                file.write('')

    def test_unzip(self):
        archive_zip_path = path.join(self.test_data, 'page_test.zip')
        archive_rar_path = path.join(self.test_data, 'page_test.rar')

        with self.subTest('Unzip file'):
            unzip(archive_zip_path)
            folder = path.splitext(archive_zip_path)[0]
            self.assertTrue(path.exists(folder))

            rmtree(folder)

        with self.subTest('Custom save path'):
            save_path = path.join(getcwd(), 'app', 'tests', 'test_data', 'test')
            unzip(archive_zip_path, save_path)
            self.assertTrue(path.exists(save_path))

            rmtree(save_path)

        with self.subTest('Unzip with invalid archive path'):
            with self.assertRaises(InvalidArchivePathException):
                unzip('')

        with self.subTest('Unzip with nonexistent archive path'):
            with self.assertRaises(ArchivePathNotFoundException):
                unzip('test_archive.zip', '')

        with self.subTest('Unzip with nonexistent archive path'):
            with self.assertRaises(UnsupportedArchiveFormatException):
                unzip(archive_rar_path)

    def test_search_folder_key_file_paths(self):
        test_dir = path.join(self.test_data, 'test_dir')

        with self.subTest('Search folder key file paths'):
            self.create_pages_structure(test_dir, 'index.html', 3)
            index_paths = search_folder_key_file_paths(test_dir, 'index.html')

            self.assertTrue(3, len(index_paths))
            for index_path in index_paths:
                with self.subTest(string=path):
                    self.assertIn('index.html', index_path)

            rmtree(test_dir)

        with self.subTest('Empty folder_path'):
            paths = search_folder_key_file_paths('', 'index.html')
            self.assertIsNone(paths)

        with self.subTest('Empty key_file'):
            paths = search_folder_key_file_paths(test_dir, '')
            self.assertIsNone(paths)

        with self.subTest('Incorrect path folder_path'):
            paths = search_folder_key_file_paths('invalid_path', 'index.html')
            self.assertIsNone(paths)

        with self.subTest('Key not found, empty list'):
            self.create_pages_structure(test_dir, 'other.html', 3)
            paths = search_folder_key_file_paths(test_dir, 'index.html')
            self.assertIsNone(paths)

            rmtree(test_dir)
