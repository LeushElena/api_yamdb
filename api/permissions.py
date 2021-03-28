from rest_framework import permissions
from rest_framework.response import Response
from .models import CustomUser

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser or request.user.role==CustomUser.ROLE_ADMIN)
