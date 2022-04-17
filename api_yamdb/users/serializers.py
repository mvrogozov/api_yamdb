from rest_framework import serializers

from .models import User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from .models import Category, Comment, Genre, Review, Title

ROLES = (
    ("user", "User"),
    ("moderator", "Moderator"),
    ("admin", "Administrator"),
    ("superuser", "Superuser"),
)


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Нельзя использовать зарезервированное имя 'me'"
            )
        return value


class AuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=200)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=ROLES, default='user')

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
        if value == "me":
            raise serializers.ValidationError(
                "Нельзя использовать зарезервированное имя 'me'"
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="author")

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="author")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
