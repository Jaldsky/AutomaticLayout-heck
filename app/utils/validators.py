from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(RegexValidator):
    regex = r"^[\w.]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0


@deconstructible
class EmailValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9._%]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    message = _(
        "Enter a valid email address. This value may contain only letters, "
        "numbers, and @/./_ characters."
    )
    flags = 0
