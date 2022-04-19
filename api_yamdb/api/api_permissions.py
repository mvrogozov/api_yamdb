from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, obj):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin' or request.user.is_superuser


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or not request.user.is_anonymous
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (
            obj.author == request.user
            or request.user.role in ['moderator', 'admin', 'superuser']
        )
