
from rest_framework import permissions

class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_company
        except:
            return False