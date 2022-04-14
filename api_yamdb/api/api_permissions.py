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


class IsAdmin(permissions.BasePermission):

    message = 'Нет прав доступа к этому ресурсу'

    def has_permission(self, request, obj):
        return request.user.role == 'admin'
    
