from django.db import models


def get_upload_to(instance, filename):
    return instance.upload_to + filename


class UploadedFile(models.Model):
    file = models.FileField(upload_to=get_upload_to, default=None)
    name = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=10, default=None)
    upload_to = ""

    def save_file(self, file):
        self.file.save(file.name, file, save=True)

    def delete_file(self):
        self.file.delete(save=True)
