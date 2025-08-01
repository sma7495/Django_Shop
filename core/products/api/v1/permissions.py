# permissions.py
from rest_framework import permissions

class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Allows access only to admin users (is_staff=True) or superusers.
    """
    def has_permission(self, request, view):
        try:
            if request.user.type == 2 or request.user.type == 3:
                return True
        except:
            pass
        return False



class IsProductOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to only allow owners of a product or admins to modify/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin/superuser always has permission
        if request.user.is_superuser:
            return True
            
        # Check if the requesting user is the product owner
        return obj.user == request.user