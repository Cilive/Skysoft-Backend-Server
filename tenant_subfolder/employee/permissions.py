
from rest_framework import permissions

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_employee
        except:
            return False