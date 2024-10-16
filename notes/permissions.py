from rest_framework.permissions import BasePermission


class IsAdminUserOrOwner(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser
        return True
    
    def has_object_permission(self, request, view, obj):
         return obj.owner == request.user or request.user.is_superuser