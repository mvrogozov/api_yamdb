

from reviews.models import Title, Category, Genre

from email.policy import default
from rest_framework import serializers
from reviews.models import User, Review, Comment
from rest_framework.relations import SlugRelatedField

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


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать зарезервированное имя \'me\''
            )
        return value



class AuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=200)
    confirmation_code = serializers.CharField(max_length=200)


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=User.ROLES, default='user')

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать зарезервированное имя \'me\''
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='author')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='author')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment

