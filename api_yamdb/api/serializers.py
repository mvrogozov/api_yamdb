from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment


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
