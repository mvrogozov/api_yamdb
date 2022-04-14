from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.db.models import CheckConstraint, Q, F



class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name="titles")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="titles",
    )

    def __str__(self):
        return self.name

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
        max_length=21,
        choices=ROLES,
        blank=True,
        default='user'
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username='me'),
                name='name_not_me'
            )
        ]

 
class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerChoices('Оценка', '1 2 3 4 5 6 7 8 9 10')
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

