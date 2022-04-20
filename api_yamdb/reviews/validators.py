from django.forms import ValidationError
from django.utils import timezone


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Wrong year!'),
            params={'value': value},
        )
