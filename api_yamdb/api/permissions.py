from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

ERROR_MESSAGES = {
    'update_denied': 'Изменение чужого контента запрещено!',
    'delete_denied': 'Удаление чужого контента запрещено!'
}


class ReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            if request.method in ['PUT', 'PATCH']:
                raise PermissionDenied(ERROR_MESSAGES['update_denied'])
            if request.method in ['DELETE']:
                raise PermissionDenied(ERROR_MESSAGES['delete_denied'])
        return True


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_moderator:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            if request.method in ['PUT', 'PATCH']:
                raise PermissionDenied(ERROR_MESSAGES['update_denied'])
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return False


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.is_moderator
                                              or request.user.is_admin):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user and request.user.is_moderator:
            if request.method in ['PUT', 'PATCH']:
                raise PermissionDenied(ERROR_MESSAGES['update_denied'])
        return True
