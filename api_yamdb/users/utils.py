from rest_framework import serializers


def is_me(value):
    if value == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать зарезервированное имя "me"'
        )
    return value
