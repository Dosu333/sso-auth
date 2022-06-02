from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsSuperAdmin(permissions.BasePermission):
    """Allows access only to super admin users. """
    message = "Only Super Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'SUPERADMIN' in request.user.roles)


class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users. """
    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'ADMIN' in request.user.roles)


class IsRegularUser(permissions.BasePermission):
    """Allows access only to talent users. """
    message = "Only Regular users are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'REGULAR' in request.user.roles)

class IsRestaurant(permissions.BasePermission):
    """Allows access only to restaurants. """
    message = "Only Restaurants are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'RESTAURANT' in request.user.roles)


class IsConsumer(permissions.BasePermission):
    """Allows access only to consumers. """
    message = "Only Consumers are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'CONSUMER' in request.user.roles)
        

class IsDriver(permissions.BasePermission):
    """Allows access only to Drivers. """
    message = "Only Drivers are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'DRIVER' in request.user.roles)


class IsOrderAdmin(permissions.BasePermission):
    """Allows access only to OrderAdmins. """
    message = "Only Order Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'ORDERADMIN' in request.user.roles)

class IsStoreOwner(permissions.BasePermission):
    """Allows access only to Store owners. """
    message = "Only Store owners are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'STORE_OWNER' in request.user.roles)