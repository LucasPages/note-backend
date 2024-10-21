from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_superuser
        return True
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.id == request.user.id or request.user.is_superuser
        return obj.id == request.user.id


class IsAuthorOfNote(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_superuser
        return True
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminUserOrOwner(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and request.user.is_superuser
        return True
    
    def has_object_permission(self, request, view, obj):
         return obj.owner == request.user or request.user.is_superuser