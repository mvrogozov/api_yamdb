from rest_framework import serializers
from reviews.models import User


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=200)
    confirmation_code = serializers.CharField(max_length=200)
