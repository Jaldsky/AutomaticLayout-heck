from unittest import TestCase
from os import path, getcwd, remove

from app.engine.util import unzip


class UtilTest(TestCase):

    def test_unzip(self):
        test_archive_path = path.join(getcwd(), 'app', 'tests', 'test_data')
        unzip(test_archive_path)
