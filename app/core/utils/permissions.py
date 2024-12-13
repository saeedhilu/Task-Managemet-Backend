from rest_framework import permissions

class IsAdminAndAuthenticated(permissions.BasePermission):
    """
    Custom permission to grant access only to users with the 'admin' role and who are authenticated.
    """

    def has_permission(self, request,view):
        return request.user.is_authenticated and request.user.role == 'admin'
    

class IsPm(permissions.BasePermission):
    """
    Custom permission to grant access only to users with the 'project_manager' role and who are authenticated.
    """
    def has_permission(self, request,view):
        return request.user.is_authenticated and request.user.role == 'project_manager'
    

class IsMember(permissions.BasePermission):
    """
    Custom permission to grant access only to users with the 'member' role and who are authenticated.
    """
    def has_permission(self, request,view):
        return request.user.is_authenticated and request.user.role == 'member'

class AdminOrPm(permissions.BasePermission):
    """
    Custom permission to grant access only to users with the 'admin' or 'project_manager' role and who are authenticated.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'project_manager')