import datetime
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializerEdit(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        read_only_fields = ('id',)


class TitleSerializerSafe(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True, many=False)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'rating',
            'genre',
            'category',
        )
        read_only_fields = ('id', 'rating', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.datetime.now():
            raise serializers.ValidationError('Wrong year')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if 0 <= value <= 10:
            return value
        return serializers.ValidationError('Wrong score')

    def validate(self, attrs):
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        user = self.context.get('request').user
        method = self.context.get('request').method
        if (
            Review.objects.filter(title=title, author=user).exists()
                and method == 'POST'):
            raise serializers.ValidationError(
                'Только один отзыв от пользователя'
            )
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
