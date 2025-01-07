from rest_framework.permissions import BasePermission
from rest_framework import permissions
import logging
# from .userprofile import UserProfile

logger = logging.getLogger(__name__)
# class SellerUserOrRead(permissions.BasePermission):
#     def has_permission(self, request, view):
      
        
#         if request.method in permissions.SAFE_METHODS:
#             print("Permission Granted: SAFE_METHOD")
#             return True

#         if not request.user.is_authenticated:
#             print("Permission Denied: User not authenticated")
#             return False

#         # ამოწმებს, აქვს თუ არა მომხმარებელს კონკრეტული უფლება
#         has_permission = request.user.has_perm('app.add_product')
#         print(f"Has Permission ('app.add_product'): {has_permission}")

#         if has_permission:
#             print("Permission Granted: User has required permission")
#         else:
#             print("Permission Denied: User does not have required permission")

#         return has_permission
# class SellerUserOrRead(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Read-only access for safe methods
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # User must be authenticated
#         if not request.user.is_authenticated:
#             return False

#         # Check if the user is a superuser or has 'is_seller' flag set in UserProfile
#         try:
#             user_profile = request.user.userprofile
#             if request.user.is_superuser or user_profile.is_seller:
#                 return True
#         except UserProfile.DoesNotExist:
#             return False

#         return False
class SellerPermission(BasePermission):
    def has_permission(self, request, view):
        # ავთენტიკაცია უნდა იყოს მიღებული და საჭირო უფლება დადასტურებული
        return request.user.is_authenticated and (request.user.has_perm('app.add_product') or request.user.is_superuser)

# class SellerPermission(BasePermission):
#     def has_permission(self, request, view):
#         # სელერი მომხმარებლისთვის - როგორც ალტერნატივა, შეგიძლიათ შეამოწმოთ `is_seller`
#         if request.user.is_authenticated:
#             return request.user.is_superuser or getattr(request.user, 'userprofile', None).is_seller
#         return False
