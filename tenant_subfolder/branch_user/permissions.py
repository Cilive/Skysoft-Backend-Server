
from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_branch_user
        except:
            return False