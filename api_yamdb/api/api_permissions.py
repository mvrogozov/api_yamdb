from email import message
from rest_framework import permissions
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        )


class PostOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        return request.method == 'POST'