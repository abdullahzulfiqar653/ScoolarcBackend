from django.apps import apps
from django.db.models import Q
from rest_framework import permissions, exceptions


class isMerchantMember(permissions.BasePermission):
    message = "You do not have permission to access this merchant's resources."

    def has_permission(self, request, view):
        if not request.merchant:
            return False
        if request.user.profile.merchant != request.merchant:
            return False
        return True


class IsMerchantMemberAnonymous(permissions.BasePermission):
    """
    Permission to check if the Anonymous user is a member of the merchant,
    even for anonymous requests where email or phone is provided.
    """

    def has_permission(self, request, view):
        if not hasattr(request, "merchant") or not request.merchant:
            raise exceptions.NotFound({"detail": ["Entity not found."]})

        username = request.data.get("username", "")

        query = request.merchant.members.filter(
            Q(user__email=username) | Q(user__username=username),
        )

        if not query.exists():
            raise exceptions.NotFound({"username": ["User not found."]})
        request.member = query.first()
        return True


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
                classes = None
                section = None

            case str(s) if s.startswith("/api/classes/"):
                if not hasattr(request, "classes"):
                    Classes = apps.get_model("api", "Classes")
                    class_id = view.kwargs.get("pk") or view.kwargs.get("id")
                    request.classes = get_instance(
                        Classes.objects.select_related("outlet__merchant"), class_id
                    )
                classes = request.classes
                outlet = classes.outlet
                merchant = outlet.merchant
                section = None

            case str(s) if s.startswith("/api/sections/"):
                if not hasattr(request, "section"):
                    Sections = apps.get_model("api", "Sections")
                    section_id = view.kwargs.get("pk") or view.kwargs.get("id")
                    request.section = get_instance(
                        Sections.objects.select_related("classes__outlet__merchant"),
                        section_id,
                    )
                section = request.section
                classes = section.classes
                outlet = classes.outlet
                merchant = outlet.merchant

            case _:
                outlet = None
                merchant = None
                classes = None
                section = None

        return merchant, outlet, classes, section

    def is_authenticated(self, request):
        return bool(request.user and request.user.is_authenticated)

    def is_in_outlet(self, request, view):
        if not self.is_authenticated(request):
            return False

        merchant, outlet, classes, sections = self.get_merchant_outlet(request, view)
        if outlet:
            if outlet in request.user.profile.outlets.all():
                if classes:
                    if classes in outlet.outlet_classes.all():
                        return classes
                elif sections:
                    if sections in classes.sections.all():
                        return sections
                else:
                    return outlet
                return outlet
            else:
                raise exceptions.NotFound
        return False

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


class IsOutletMember(InOutletOrMerchant):
    def has_permission(self, request, view):
        outlet = self.is_in_outlet(request, view)
        print(outlet)
        if not outlet:
            return False
        return True


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        method_perms = {
            "GET": "view",
            "POST": "add",
            "PUT": "change",
            "PATCH": "change",
            "DELETE": "delete",
        }
        model = view.get_queryset().model if hasattr(view, "get_queryset") else None
        if model:
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            action = method_perms.get(request.method, "view")
            permission_codename = f"{app_label}.{action}_{model_name}"
            return request.user.has_perm(permission_codename)
        return False
