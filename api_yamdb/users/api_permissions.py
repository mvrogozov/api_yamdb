from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, obj):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser
