from email.policy import default

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User

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

    role = serializers.ChoiceField(choices=ROLES, default="user")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "bio",
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


class TitleSerializerEdit(serializers.ModelSerializer):
    genre = SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")
        read_only_fields = ("id",)


class TitleSerializerSafe(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True, many=False)
    rating = serializers.IntegerField(read_only=True)

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
