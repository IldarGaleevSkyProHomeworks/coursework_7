from django.contrib.auth.models import User
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        return obj.owner == request.user if hasattr(obj, 'owner') else False


class IsAnonCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user:
            return True
        return False
