from email.policy import default
from rest_framework import serializers
from reviews.models import User


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
