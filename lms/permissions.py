from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'У Вас нет прав доступа на это действие!'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()
