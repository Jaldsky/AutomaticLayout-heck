from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from app.utils.validators import EmailValidator, UsernameValidator


# from django.db.models.signals import pre_delete, pre_save, post_save
# from django.dispatch import receiver

# FILE_TYPES = (
#     ('RAR', 'RAR'),
#     ('ZIP', 'ZIP'),
#     ('PNG', 'PNG'),
#     ('JPEG', 'JPEG'),
# )
#
# COMPARATION_METHOD = (
#     ('MSE', 'MSE'),
#     ('SSIM', 'SSIM'),
#     ('VGG16', 'VGG16'),
# )


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class AuthUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()
    email_validator = EmailValidator()

    username = models.CharField(
        max_length=25, unique=True, validators=[username_validator],
        help_text=(
            "Required 25 characters or fewer. Letters, digits and . _ only."
        ),
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(
        max_length=50, unique=True, validators=[email_validator],
        help_text=(
            "Required 50 characters or fewer. Letters, digits and @ . _ only."
        ),
        error_messages={
            "unique": "Invalid email.",
        },
    )

    is_staff = models.BooleanField(default=True)  # can the user log in
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

#
#
# class UserSession(models.Model):
#     """Represents a user session in the system.
#     This model is used to store information about user sessions,
#     including the associated user and session ID.
#
#     Attributes:
#         user: The user associated with the session.
#         session_id: The ID of the session.
#         uuid: The UUID of the cache.
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     session_id = models.CharField(max_length=255, blank=True, null=True)
#     uui = models.CharField(max_length=32, default=None, blank=True, null=True)
#
#     def __str__(self):
#         return f'{self.user.username}\'s Session'
#
#
# class UserSettings(models.Model):
#     """Represents user-specific settings in the system.
#     This model stores settings for individual users, including cache settings,
#     text visibility preferences, and comparators for image processing.
#
#     Attributes:
#         user: The user to whom the settings belong.
#         clear_cache: Flag indicating whether to clear the cache.
#         hide_text: Flag indicating whether text on an image should be hidden.
#         mse: Flag indicating whether to use Mean Squared Error as a comparator.
#         ssim: Flag indicating whether to use Structural Similarity Index as a comparator.
#         vgg16: Flag indicating whether to use the VGG16 neural network as a comparator.
#     """
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#
#     clear_cache = models.BooleanField(default=True)
#     hide_text = models.BooleanField(default=False)
#
#     mse = models.BooleanField(default=True)
#     ssim = models.BooleanField(default=True)
#     vgg16 = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f'{self.user.username}\'s Settings'
#
#
# class Comparison(models.Model):
#     """Represents a comparison operation initiated by a user.
#     This model is used to store information about comparisons performed by users,
#     including the associated user session, cache UUID, and timestamp.
#
#     Attributes:
#         user_session: The user session associated with the comparison.
#         uuid: The UUID of the cache.
#         create: Timestamp indicating when the comparison process was created.
#         update: Timestamp indicating when the comparison was performed.
#         method: The method used for comparison.
#         threshold: The threshold value used in the comparison.
#         value: An integer value associated with the comparison.
#         percentages: A floating-point value representing percentages related to the comparison.
#         is_similar: Boolean indicating whether the comparison resulted in similarity (True) or dissimilarity (False).
#     """
#     user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='comparisons')
#     uui = models.CharField(max_length=32, blank=True, null=True)
#
#     create = models.DateTimeField(auto_now=True)
#     update = models.DateTimeField(auto_now=True)
#
#     method = models.CharField(choices=COMPARATION_METHOD, max_length=10, default=None, blank=True, null=True)
#     threshold = models.FloatField(default=None, blank=True, null=True)
#
#     value = models.FloatField(default=None, blank=True, null=True)
#     percentages = models.FloatField(default=None, blank=True, null=True)
#     is_similar = models.BooleanField(default=None, blank=True, null=True)
#
#     # ['id', 'user_id', 'uui', 'create', 'update', 'method', 'threshold', 'is_similar']
#
#
# class UploadedFile(models.Model):
#     """Represents a file uploaded by a user.
#     This model is used to store information about files uploaded by users,
#     including the file itself, its name, type, and upload date.
#
#     Attributes:
#         user: The user associated with the session.
#         file: The uploaded file.
#         name: The name of the file.
#         type: The type of the file.
#         datetime: The date and time when the file was uploaded.
#     """
#     # user = models.OneToOneField(User, on_delete=models.CASCADE, to_field='id')
#
#     file = models.FileField(default=None)
#     name = models.CharField(max_length=255, default=None)
#     type = models.CharField(max_length=10, choices=FILE_TYPES, default=None)
#     datetime = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f'{self.name} ({self.datetime})'
#
#
# @receiver(pre_save, sender=Comparison)
# def set_comparison_uui(sender, instance, **kwargs):
#     if not instance.uui and instance.user_session:
#         instance.uui = instance.user_session.uui
#
#
# @receiver(post_save, sender=UserSession)
# def update_comparison_uui(sender, instance, **kwargs):
#     Comparison.objects.filter(user_session=instance).update(uui=instance.uui)
#
#
# @receiver(pre_delete, sender=UserSession)
# def delete_comparisons(sender, instance, **kwargs):
#     Comparison.objects.filter(user_session=instance).delete()
