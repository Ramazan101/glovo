from rest_framework.permissions import BasePermission

class ChekRolePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'

class ChekCourierPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'courier'

class CreateStorePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'