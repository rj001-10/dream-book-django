from rest_framework.permissions import BasePermission
class IsAdminOrLoggedInUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj == request.user
        
    