from django.apps import apps

from rest_framework import permissions, exceptions


class MerchantDomainPermission(permissions.BasePermission):
    message = "You do not have permission to access this merchant's resources."

    def has_permission(self, request, view):
        if not request.merchant:
            return False

        if request.user.profile.merchant != request.merchant:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        is_merchant = request.user.profile.role.name in ["Merchant"]
        if request.method == "POST":
            return is_merchant

        return is_merchant

    # def has_object_permission(self, request, view, obj):
    #     if obj.merchant != request.merchant:
    #         return False

    #     if request.method in ["PUT", "PATCH", "DELETE"]:
    #         return request.user.profile.role.name in ["Merchant"]

    #     return True


def get_instance(queryset, instance_id):
    try:
        instance = queryset.get(id=instance_id)
    except queryset.model.DoesNotExist:
        raise exceptions.NotFound
    return instance


class InOutletOrMerchant(permissions.BasePermission):
    def get_merchant_outlet(self, request, view):
        match request.path:
            case str(s) if s.startswith("/api/outlets/"):
                if not hasattr(request, "outlet"):
                    Outlet = apps.get_model("api", "Outlet")
                    outlet_id = view.kwargs.get("pk") or view.kwargs.get("outlet_id")
                    queryset = Outlet.objects.select_related("merchant")
                    request.outlet = get_instance(queryset, outlet_id)
                outlet = request.outlet
                merchant = outlet.merchant

            case _:
                outlet = None
                merchant = None

        return merchant, outlet

    def is_authenticated(self, request):
        return bool(request.user and request.user.is_authenticated)

    def is_in_outlet_or_merchant(self, request, view):
        if not self.is_authenticated(request):
            return False

        merchant, outlet = self.get_merchant_outlet(request, view)
        if outlet:
            if outlet in request.user.profile.outlets.all():
                return outlet.merchant
            else:
                raise exceptions.NotFound
        elif merchant:
            if merchant.members.filter(user=request.user):
                return merchant
            else:
                raise exceptions.NotFound
        else:
            return False


class IsMerchantOwner(InOutletOrMerchant):
    def has_permission(self, request, view):
        merchant = self.is_in_outlet_or_merchant(request, view)
        if not merchant:
            return False

        if hasattr(merchant, "owner") and merchant.owner == request.user:
            return True
        else:
            return False


class IsOutletEditor(InOutletOrMerchant):
    def has_permission(self, request, view):
        merchant = self.is_in_outlet_or_merchant(request, view)
        if not merchant:
            return False

        role = request.user.get_role(merchant)
        # if role == WorkspaceUser.Role.EDITOR:
        #     return True
        # else:
        #     return False
