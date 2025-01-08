from rest_framework.permissions import BasePermission
from rest_framework import permissions


class SellerPermission(BasePermission):
    def has_permission(self, request, view):
        # ავთენტიკაცია უნდა იყოს მიღებული და საჭირო უფლება დადასტურებული
        return request.user.is_authenticated and (request.user.has_perm('app.add_product') or request.user.is_superuser)

