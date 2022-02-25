from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    def has_permission(self,request,view):
        try:
            return request.user.is_superuser
        except:
            return False


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_company
        except:
            return False