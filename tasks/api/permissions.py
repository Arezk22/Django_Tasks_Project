from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):    
    message = "You must be the owner of this object or an admin to access it."
    def has_object_permission(self, request, view, obj):
        # Allow access if the user is an admin
        if request.user.is_staff:
            return True
        # Allow access if the user is the owner of the object
        return obj.user == request.user