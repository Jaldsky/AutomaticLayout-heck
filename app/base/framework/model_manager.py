from django.apps import apps
from django.db.models import Model

from app.base.exceptions import ModelManagerException, ModelManagerMessages
from app.base.types import ModelName, DefaultArgs


class ModelManager:
    exception = ModelManagerException
    messages = ModelManagerMessages

    def get_model_by_name(self, model_name: ModelName) -> Model:
        """Метод получения модели по названию.

        Args:
            model_name: Название модели, начиная с названия проекта (например, app.mymodel).

        Returns:
            Объект модели
        """
        if not isinstance(model_name, ModelName):
            raise self.exception(self.messages.INVALID_MODEL_NAME_TYPE_ERROR)

        try:
            return apps.get_model(model_name)
        except Exception:
            raise self.exception(self.messages.GET_MODEL_ERROR)

    def get_or_create_model_object(self, model_name: ModelName, defaults: DefaultArgs = None, **kwargs,):
        pass


        # Model = apps.get_model(model_name)
        # obj, created = Model.objects.get_or_create(defaults=defaults, **kwargs)
        # return obj, created

        # Model = apps.get_model(model_name)
        #
        # model.objects.get_or_create(defaults=defaults, name='Some Name')
        #
        # return model.objects.get_or_create(username=request.user)[0]
