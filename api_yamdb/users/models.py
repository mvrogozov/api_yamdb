from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q


class User(AbstractUser):

    ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
        ('superuser', 'Superuser'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150, unique=False, blank=True, null=True
    )
    last_name = models.CharField(
        max_length=150, unique=False, blank=True, null=True
    )

    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(
        max_length=150, unique=False, blank=True, null=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=21, choices=ROLES, blank=True, default='user'
    )

    class Meta:
        constraints = [
            CheckConstraint(check=~Q(username='me'), name='name_not_me')
        ]
