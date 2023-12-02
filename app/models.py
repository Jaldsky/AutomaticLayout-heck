from django.db import models


def get_upload_to(instance, filename):
    return instance.upload_to + filename


class UploadedFile(models.Model):
    """Модель для загрузки файлов."""
    file = models.FileField(upload_to=get_upload_to, default=None)
    name = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=10, default=None)
    upload_to = ""
    upload_data = models.DateTimeField(auto_now=True)

    def save_file(self, file):
        self.file.save(file.name, file, save=True)

    def delete_file(self):
        self.file.delete(save=True)


class ProjectSettings(models.Model):
    """Модель для настроек сравнения изображений."""
    bedaub_text = models.BooleanField(default=False)
    clear_local_cache = models.BooleanField(default=True)
    mse_comparator = models.BooleanField(default=True)
    ssim_comparator = models.BooleanField(default=True)
    vgg16_comparator = models.BooleanField(default=True)

    @staticmethod
    def bool_to_lowercase_str(choice):
        return str(choice).lower()

    def __str__(self):
        bedaub_text = self.bool_to_lowercase_str(self.bedaub_text)
        clear_local_cache = self.bool_to_lowercase_str(self.clear_local_cache)
        mse_comparator = self.bool_to_lowercase_str(self.mse_comparator)
        ssim_comparator = self.bool_to_lowercase_str(self.ssim_comparator)
        vgg16_comparator = self.bool_to_lowercase_str(self.vgg16_comparator)

        return '{"bedaub_text": %s, "clear_local_cache": %s, "mse_comparator": %s,' \
               '"ssim_comparator": %s, "vgg16_comparator": %s}' % (bedaub_text, clear_local_cache, mse_comparator,
                                                                   ssim_comparator, vgg16_comparator)
