from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
        ('superuser', 'Superuser')
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True
    )

    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default='user'
    )
