from rest_framework import serializers

from .models import User
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
