from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import year_validator


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        unique=True,
        db_index=True
    )
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        unique=True,
        db_index=True
    )
    slug = models.SlugField('slug', max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256, db_index=True)
    year = models.IntegerField(
        'Год',
        validators=[year_validator, ]
    )
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('дата', auto_now_add=True)
    score = models.IntegerField(
        'Оценка',
        validators=[
            MaxValueValidator(10, 'Value error'),
            MinValueValidator(0, 'Value error'),
        ]
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField('текст')
    pub_date = models.DateTimeField('дата', auto_now_add=True)

    class Meta:

        ordering = ('pub_date',)

    def __str__(self):
        return self.text
