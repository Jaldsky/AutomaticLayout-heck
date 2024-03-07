from unittest import TestCase
from os import path, getcwd, makedirs
from shutil import rmtree
from random import choices
from string import ascii_lowercase


from app.engine.util import (
    unzip,
    search_folder_key_file_paths,
    UnZipFileException
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

    def test_search_folder_key_file_paths(self):
        test_dir = path.join(self.test_data, 'test_dir')

        with self.subTest('Search folder key file paths'):
            self.create_pages_structure(test_dir, 'index.html', 3)
            index_paths = search_folder_key_file_paths(test_dir, 'index.html')

            self.assertTrue(3, len(index_paths))
            for index_path in index_paths:
                with self.subTest(string=path):
                    self.assertIn('index.html', index_path, f"Файл '{index_path}' не содержит 'index.html'")

            rmtree(test_dir)

        # TODO add test cases:
        # 1. Empty folder_path
        # 2. Empty key_file
        # 3. Incorrect path folder_path
        # 4. Key not found, empty list
