from unittest import TestCase

from django.db.models.base import ModelBase
from app.base.framework.model_manager import ModelManager


class TestModelManager(TestCase):

    def setUp(self) -> None:
        self.instance = ModelManager()
        self.exception = self.instance.exception
        self.messages = self.instance.messages

    def test_get_model_by_name(self) -> None:
        with self.subTest("Get model by name"):
            self.assertTrue(issubclass(type(self.instance.get_model_by_name("app.AuthUser")), ModelBase))

        with self.subTest("Invalid model name, non-existent table"), self.assertRaises(self.exception) as e:
            _ = self.instance.get_model_by_name("test")
        self.assertEqual(self.messages.GET_MODEL_ERROR, e.exception.message)

        with self.subTest("Invalid model name, unknown type"), self.assertRaises(self.exception) as e:
            _ = self.instance.get_model_by_name(None)
        self.assertEqual(self.messages.INVALID_MODEL_NAME_TYPE_ERROR, e.exception.message)

    def test_get_or_create_model_object(self):
        with self.subTest("Get model object"):
            pass

        #     with self.subTest("Get model by name"):
        #         self.assertIsInstance(self.instance.get_model_by_name("app.AuthUser"), class_)
        #
        #     model = self.instance.get_model_by_name("app.AuthUser")
        #     # Проверка соответствия типа объекта model и класса AuthUser
        #     self.assertIsInstance(model, models.AuthUser)
        #     # self.assertIsInstance(self.instance.get_model_by_name("app.AuthUser"), .AuthUser)
        #
        # #     self.assertIsInstance(self.instance.open_image( self.img_path), PSDImage)
        #
        # with self.subTest("Invalid image path"), self.assertRaises(self.exception) as e:
        #     _ = self.instance.open_image("test")
        # self.assertEqual(self.messages.INVALID_IMG_PATH_ERROR, e.exception.message)