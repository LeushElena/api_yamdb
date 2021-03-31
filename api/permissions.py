from rest_framework import permissions
from rest_framework.response import Response
from .models import CustomUser

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.is_superuser or 
                request.user.role==CustomUser.ROLE_ADMIN)


MODERATOR_METHODS = ('PATCH', 'DELETE')


class IsAdminOrAccessDenied(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == CustomUser.ROLE_ADMIN
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == CustomUser.ROLE_ADMIN
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == CustomUser.ROLE_ADMIN
                or request.user.is_superuser)


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in MODERATOR_METHODS
                and request.user.role == CustomUser.ROLE_MODERATOR
                or obj.author == request.user)
