from rest_framework import permissions

from users.models import User


class AdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user and request.user.is_staff)

class RegistredUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS 
        or obj.author == request.user)