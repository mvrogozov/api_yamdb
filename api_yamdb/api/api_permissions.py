from rest_framework import permissions


class IsOwnerU(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'create']:
            if request.user.is_anonymous:
                return False
            return request.user.role == 'admin' or request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        return (
            view.action in ['retrieve', 'partial_update']
            and (
                obj.username == request.user.username
                or request.user.role == 'admin'
                or request.user.is_superuser
            )
        ) or (
            view.action == 'destroy'
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, obj):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin'
