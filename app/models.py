from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.db import models

from app.constants import MODEL_FILE_TYPE, MODEL_COMPARISON_METHOD
from app.utils.validators import EmailValidator, UsernameValidator


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


class UserSettings(models.Model):
    """Represents user-specific settings in the system.
    This model stores settings for individual users, including cache settings,
    text visibility preferences, and comparators for image processing.

    Attributes:
        username: The user to whom the settings belong.
        clear_cache: Flag indicating whether to clear the cache.
        hide_text: Flag indicating whether text on an image should be hidden.
        mse: Flag indicating whether to use Mean Squared Error as a comparator.
        ssim: Flag indicating whether to use Structural Similarity Index as a comparator.
        vgg16: Flag indicating whether to use the VGG16 neural network as a comparator.
    """
    username = models.ForeignKey(AuthUser, on_delete=models.CASCADE, primary_key=True)

    clear_cache = models.BooleanField(default=False)
    hide_text = models.BooleanField(default=False)

    mse = models.BooleanField(default=False)
    ssim = models.BooleanField(default=False)
    vgg16 = models.BooleanField(default=False)

    def __str__(self):
        return (
            'Current settings: '
            f'clear_cache is {self.clear_cache}, '
            f'hide_text is {self.hide_text}, '
            f'mse is {self.mse}, '
            f'ssim is {self.ssim}, '
            f'vgg16 is {self.vgg16}'
        )


class UserUploadFile(models.Model):
    """Represents a file uploaded by a user.
    This model is used to store information about files uploaded by users,
    including the file itself, its name, type, and upload date.
    """
    username = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    file = models.FileField()
    timestamp = models.DateTimeField(auto_now=True)
    file_type = models.CharField(choices=MODEL_FILE_TYPE, max_length=5)
    uuid = models.CharField(max_length=36)

    def __str__(self):
        return f'{self.uuid} ({self.file_type}/{self.timestamp})'


class ComparisonResults(models.Model):
    """Represents a comparison operation initiated by a user.
    This model is used to store information about comparisons performed by users,
    including the associated user session, cache UUID, and timestamp.
    """
    username = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now=True)
    uuid_reference = models.CharField(max_length=36)
    uuid_compared = models.CharField(max_length=36)

    method = models.CharField(choices=MODEL_COMPARISON_METHOD, max_length=5)
    value = models.FloatField()
    threshold = models.FloatField()

    is_similar = models.BooleanField()
