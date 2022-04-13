from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLES = (
        ('ANON', 'Anonymous'),
        ('USER', 'User'),
        ('MODER', 'Moderator'),
        ('ADMIN', 'Administrator'),
        ('SUDJANGO', 'Superuser')
    )

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default='USER'
    )
