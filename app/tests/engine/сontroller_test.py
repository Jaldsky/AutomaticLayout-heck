import os
import shutil
from unittest import TestCase
from unittest.mock import patch

from django.contrib.auth.models import User

from app.engine.util import remove_folder_or_file, join_path, create_folder
from app.engine.сontroller import CompareController
from app.models import UserSession, Comparation, UserSettings

test_data = os.path.join(os.getcwd(), 'app', 'tests', 'test_data')


class ControllerTest(TestCase):
    _patcher = None

    @classmethod
    def setUpClass(cls) -> None:
        cls._patcher = patch(
            'app.engine.сontroller.CACHE_PATH', new=test_data
        )

        cls._patcher.start()

    def setUp(self) -> None:
        if not User.objects.filter(id=10).exists():
            user = User.objects.create(id=10, username='bob_tester')
            user_session = UserSession.objects.create(user=user)
            Comparation.objects.create(user=user_session, uui='7fbc1219-62e3-4aa7-a5fe-cb2629d03579')

    def test_get_rendered_sits_image_paths(self):
        # create cache folder
        cache_path = join_path([test_data, '7fbc1219-62e3-4aa7-a5fe-cb2629d03579'])
        create_folder(cache_path)
        # copy and move archive
        source_path = join_path([test_data, 'page_test.zip'])
        destination_path = join_path([cache_path, 'archive.zip'])
        shutil.copy(source_path, destination_path)

        controller = CompareController(user_id=10)
        controller.get_rendered_sits_image_paths()

        self.assertTrue(os.path.isfile(join_path([cache_path, 'site_image_0.png'])))

        # remove cache data
        remove_folder_or_file(cache_path)

    def test_get_reference_image_path(self):
        # create cache folder
        cache_path = join_path([test_data, '7fbc1219-62e3-4aa7-a5fe-cb2629d03579'])
        create_folder(cache_path)
        # copy and move psd-file
        source_path = join_path([test_data, 'template_test.psd'])
        destination_path = join_path([cache_path, 'template.psd'])
        shutil.copy(source_path, destination_path)

        controller = CompareController(user_id=10)
        controller.get_reference_image_path()

        self.assertTrue(os.path.isfile(join_path([cache_path, 'reference_image.png'])))

        # remove cache data
        remove_folder_or_file(cache_path)

    def tearDown(self) -> None:
        User.objects.get(id=10).delete()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._patcher.stop()
