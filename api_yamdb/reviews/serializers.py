from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializerEdit(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id", "name", "year", "description", "genre", "category", "rating"
        )
        read_only_fields = ("id",)

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))


class TitleSerializerSafe(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True, many=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "rating",
            "genre",
            "category",
        )
        read_only_fields = ("id", "rating", "genre", "category")

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, attrs):
        title = get_object_or_404(
            Title,
            pk=self.context['view'].kwargs.get('title_id')
        )
        user = self.context.get('request').user
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                'Только один отзыв от пользователя'
            )
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="author")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
