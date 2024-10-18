from rest_framework import permissions


class MerchantDomainPermission(permissions.BasePermission):
    message = "You do not have permission to access this merchant's resources."

    def has_permission(self, request, view):
        if not request.merchant:
            return False

        if request.user.member_profile.merchant != request.merchant:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        is_merchant = request.user.member_profile.role.name in ["Merchant"]
        if request.method == "POST":
            return is_merchant

        return is_merchant

    def has_object_permission(self, request, view, obj):
        if obj.merchant != request.merchant:
            return False

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user.member_profile.role.name in ["Merchant"]

        return True
