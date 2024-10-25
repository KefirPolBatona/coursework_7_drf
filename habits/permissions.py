from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Проверяет текущего пользователя на соответствие владельцу.
        """

        return obj.user == request.user
