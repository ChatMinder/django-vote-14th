from rest_framework.permissions import BasePermission

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated and request.user.is_superuser
        
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_superuser

class IsOwnerOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj == request.user or request.user.is_superuser)