from django.db import models
from django.conf import settings


class UploadedFile(models.Model):
    file = models.FileField(upload_to=settings.UPLOADS_FILES_PATH, default=None)
    name = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=10, default=None)
