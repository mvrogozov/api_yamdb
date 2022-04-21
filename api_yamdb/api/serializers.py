from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .utils import is_me


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        return is_me(value)


class AuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=200)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=User.ROLES, default=User.USER)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'bio'
        )

    def validate_username(self, value):
        return is_me(value)


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

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError('Wrong year')
        return value


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
