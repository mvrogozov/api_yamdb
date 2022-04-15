from rest_framework import permissions


class IsOwnerU(permissions.BasePermission):

    message = 'Доступ для владельца'


    def has_permission(self, request, view):
        if view.action in ['list', 'destroy', 'create']:
            if request.user.is_anonymous:
                return False
            return request.user.role == 'admin'
        

    def has_object_permission(self, request, view, obj):
        return (
            view.action in ['retrieve', 'update', 'partial_update']
            and obj.username == request.user.username
        )
        '''return (
            obj.username == request.user.username
            and request.action == 'delete'
        )'''


class IsAdmin(permissions.BasePermission):

    message = 'Нет прав доступа к этому ресурсу'

    def has_permission(self, request, obj):
        if request.user.is_anonymous:
            return False
        return request.user.role == 'admin'
