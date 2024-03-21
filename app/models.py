from django.contrib.auth.models import User
from django.db import models


FILE_TYPES = (
    ('RAR', 'RAR'),
    ('ZIP', 'ZIP'),
    ('PNG', 'PNG'),
    ('JPEG', 'JPEG'),
)


class UserSession(models.Model):
    """Represents a user session in the system.
    This model is used to store information about user sessions,
    including the associated user and session ID.

    Attributes:
        user: The user associated with the session.
        session_id: The ID of the session.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}\'s Session'


class UserSettings(models.Model):
    """Represents user-specific settings in the system.
    This model stores settings for individual users, including cache settings,
    text visibility preferences, and comparators for image processing.

    Attributes:
        user: The user to whom the settings belong.
        cache_path: The path to the user's cache.
        clear_cache: Flag indicating whether to clear the cache.
        hide_text: Flag indicating whether text on an image should be hidden.
        mse_comparator: Flag indicating whether to use Mean Squared Error as a comparator.
        ssim_comparator: Flag indicating whether to use Structural Similarity Index as a comparator.
        vgg16_comparator: Flag indicating whether to use the VGG16 neural network as a comparator.
    """
    user = models.OneToOneField(UserSession, on_delete=models.CASCADE)

    cache_path = models.CharField(max_length=255, blank=True, null=True)
    clear_cache = models.BooleanField(default=True)
    hide_text = models.BooleanField(default=False)

    mse_comparator = models.BooleanField(default=True)
    ssim_comparator = models.BooleanField(default=True)
    vgg16_comparator = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.user.username}\'s Settings'


class UploadedFile(models.Model):
    """Represents a file uploaded by a user.
    This model is used to store information about files uploaded by users,
    including the file itself, its name, type, and upload date.

    Attributes:
        file: The uploaded file.
        name: The name of the file.
        type: The type of the file.
        datetime: The date and time when the file was uploaded.
    """
    file = models.FileField(default=None)
    name = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=10, choices=FILE_TYPES, default=None)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.datetime})'
