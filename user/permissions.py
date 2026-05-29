# from rest_framework.permissions import BasePermission
#
# class IsSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "super_user"
#
# class IsReadOnlyUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "user"

from rest_framework import permissions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL: is super user
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IsSuperUser(permissions.BasePermission):
    """
    Permission for superusers to access all data.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'superuser'
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL: Is operator
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IsOperator(permissions.BasePermission):
    """
    Permission for operators to perform safe methods and edit their own data.
    """

    def has_permission(self, request, view):
        if request.user.role != 'operator':
            return False

        # Allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow PUT and PATCH only on their own data
        return request.method in ['PUT', 'PATCH'] and view.get_object().created_by == request.user
            # return True
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL: is user
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IsUser(permissions.BasePermission):
    """
    Permission for users with role 'user' to only perform safe methods (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        return request.user.role == 'user' and request.method in permissions.SAFE_METHODS


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MODEL: combine
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# class CombinedPermission(permissions.BasePermission):
#     """
#     Combines permissions for both IsSuperUser and IsUser.
#     """
#     def has_permission(self, request, view):
#         # Allow superuser access
#         if request.user.is_superuser or request.user.role == 'superuser':
#             return True
#
#         # Check for IsUser permissions
#         if request.user.role == 'user' and request.method in permissions.SAFE_METHODS:
#             return True
#
#
#         return False
    # Check for IsUser permissions
    # if request.user.role == 'operator' and request.method in permissions.SAFE_METHODS:
    #     return True
    # return request.method in ['PUT', 'PATCH'] and view.get_object() == request.user
class ManagePermission(permissions.BasePermission):
    """
    Combines permissions for both IsSuperUser, IsOperator, and IsUser.
    """

    def has_permission(self, request, view):
        # Allow superuser access
        if request.user.is_superuser or request.user.role == 'superuser':
            return True

        # Check for IsOperator permissions
        if request.user.role == 'operator':
            # Allow safe methods
            if request.method in permissions.SAFE_METHODS:
                return True

            # Allow PUT and PATCH only on their own data
            if request.method in ['PUT', 'PATCH'] and view.get_object().created_by == request.user:
                return True

        # Check for IsUser permissions (user can only access safe methods)
        if request.user.role == 'user' and request.method in permissions.SAFE_METHODS:
            return True

        return False