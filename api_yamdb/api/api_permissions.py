from email import message
from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class IsOwnerU(permissions.BasePermission):

    message = 'Доступ для владельца'
    def has_object_permission(self, request, view, obj):
        return (
            view.action in ['retrieve', 'update', 'partial_update']
            and obj.username == request.user.username
        )
        '''return (
            obj.username == request.user.username
            and request.action == 'delete'
        )'''
        #and request.method in ('PATCH', 'PUT',)


class IsAdmin(permissions.BasePermission):

    message = 'Нет прав доступа к этому ресурсу'

    def has_permission(self, request, obj):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin'
