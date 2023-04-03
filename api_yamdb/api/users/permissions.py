from rest_framework import permissions
from api.users.models import User


class IsAdmin(permissions.BasePermission):
    """
    Пользовательское разрешение,
    позволяющее все действия Администраторам
    при любых запросах.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == User.ChoicesRole.ADMIN_ROLE
                or request.user.is_superuser
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение,
    позволяющее редактировать объект администраторам и
    смотреть всем.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.role == User.ChoicesRole.ADMIN_ROLE
                    or request.user.is_superuser
                )
            )
        )


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение позволяющее смотреть - всем,
    создавать - авторизованным пользователям,
    редактировать объект - владельцам, модераторам,
    администраторам.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == User.ChoicesRole.MODERATOR_ROLE
                or request.user.role == User.ChoicesRole.ADMIN_ROLE
                or request.user.is_superuser
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
