from rest_framework.permissions import BasePermission

class IsEducator(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'instructor':
            return True
        return False
