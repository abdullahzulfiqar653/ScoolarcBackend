from django.apps import apps
from django.db.models import Q, Prefetch
from rest_framework import permissions, exceptions
from api.models.member import Member


class isMerchantMember(permissions.BasePermission):
    message = "You do not have permission to access this merchant's resources."

    def is_authenticated(self, request):
        return bool(request.user and request.user.is_authenticated)

    def has_permission(self, request, view):
        if not self.is_authenticated(request):
            return False

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
            raise exceptions.NotFound({"detail": "Entity not found."})

        username = request.data.get("username", "")
        query = request.merchant.members.filter(
            Q(user__email=username) | Q(user__username=username),
        )

        if not query.exists():
            raise exceptions.NotFound({"username": ["User not found."]})
        request.member = query.first()
        return True


class IsParentAppRequest(permissions.BasePermission):
    """
    Permission to check if the Anonymous user is a member of the merchant,
    even for anonymous requests where email or phone is provided.
    """

    def has_permission(self, request, view):
        username = request.data.get("username", "")
        query = Member.objects.filter(primary_phone=username)

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

            case str(s) if s.startswith("/api/classes/"):
                if not hasattr(request, "classes"):
                    Classes = apps.get_model("api", "Classes")
                    class_id = view.kwargs.get("pk") or view.kwargs.get("class_id")
                    queryset = Classes.objects.select_related("outlet__merchant")
                    request.classes = get_instance(queryset, class_id)

                outlet = request.classes.outlet
                merchant = outlet.merchant

            case str(s) if s.startswith("/api/sections/"):
                if not hasattr(request, "section"):
                    Section = apps.get_model("api", "Section")
                    section_id = view.kwargs.get("pk") or view.kwargs.get("section_id")
                    request.section = get_instance(
                        Section.objects.select_related(
                            "section_class__outlet__merchant"
                        ),
                        section_id,
                    )

                outlet = request.section.section_class.outlet
                merchant = outlet.merchant

            case str(s) if s.startswith("/api/students/"):
                if not hasattr(request, "student"):
                    Student = apps.get_model("api", "Student")
                    student_id = view.kwargs.get("pk") or view.kwargs.get("student_id")
                    request.student = get_instance(
                        Student.objects.select_related(
                            "student_section__section_class__outlet__merchant",
                        ).prefetch_related("outlets"),
                        student_id,
                    )

                outlet = request.student.student_section.section_class.outlet
                merchant = outlet.merchant

            case str(s) if s.startswith("/api/parents/"):
                if not hasattr(request, "parent"):
                    Guardian = apps.get_model("api", "Guardian")
                    Student = apps.get_model("api", "Student")
                    parent_id = view.kwargs.get("pk") or view.kwargs.get("parent_id")
                    request.parent = get_instance(
                        Guardian.objects.prefetch_related(
                            Prefetch(
                                "guardian_students",
                                queryset=Student.objects.select_related(
                                    "student_section__section_class__outlet__merchant"
                                ),
                            )
                        ),
                        parent_id,
                    )
                # Now you can access easily:
                first_student = request.parent.guardian_students.first()
                outlet = first_student.student_section.section_class.outlet
                merchant = outlet.merchant

            case str(s) if s.startswith("/api/staff/"):
                if not hasattr(request, "staff"):
                    Staff = apps.get_model("api", "Staff")
                    staff_id = view.kwargs.get("pk") or view.kwargs.get("staff_id")
                    request.staff = get_instance(
                        Staff.objects.select_related(
                            "merchant"
                        ).prefetch_related(  # for ForeignKey
                            "outlets"
                        ),
                        staff_id,
                    )

                outlet = request.staff.outlets.first()
                merchant = outlet.merchant

            case str(s) if s.startswith("/api/subjects/"):
                if not hasattr(request, "subject"):
                    Subject = apps.get_model("api", "Subject")
                    subject_id = view.kwargs.get("pk") or view.kwargs.get("subject_id")
                    request.subject = get_instance(
                        Subject.objects.select_related(
                            "subject_class__outlet__merchant"
                        ),
                        subject_id,
                    )

                outlet = request.subject.subject_class.outlet
                merchant = outlet.merchant

            case _:
                outlet = None
                merchant = None

        return merchant, outlet

    def is_authenticated(self, request):
        return bool(request.user and request.user.is_authenticated)

    def is_in_outlet(self, request, view):
        if not self.is_authenticated(request):
            return False

        merchant, outlet = self.get_merchant_outlet(request, view)
        if outlet:
            if outlet in request.user.profile.outlets.all():
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
