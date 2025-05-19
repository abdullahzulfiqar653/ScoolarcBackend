from api.common.contants import PARENT
from api.models.guardian import Guardian
from api.serializers.guardian import GuardianSerializer
from api.permissions import IsOutletMember, RolePermission

from rest_framework import filters
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView


class OutletParentsListAPIView(ListAPIView):
    serializer_class = GuardianSerializer
    permission_classes = [IsOutletMember, RolePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ["address", "city", "primary_phone", "first_name", "area", "email"]

    def get_queryset(self):
        # 103bFkC8jb6cpV7
        # first_student = self.request.parent.guardian_students.first()
        # outlet = first_student.student_section.section_class.outlet
        return Guardian.objects.filter(outlets=self.request.outlet)

    @extend_schema(
        description="""
**Retrieve all Parents linked to the current outlet.**

### 🔐 Headers
- `Authorization`: Token your_auth_token *(Required)*

### 🔎 Filters Supported:
- `search`: You can search using `first_name`, `last_name`, `primary_phone`, `email`, `area`, `address`.

### 📄 Response
- Returns a list of student records"""
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OutletParentsRetrieveAPIView(RetrieveAPIView):
    serializer_class = GuardianSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_object(self):
        phone = self.kwargs.get("phone")
        try:
            parent = Guardian.objects.get(primary_phone=phone)
        except Guardian.DoesNotExist:
            raise NotFound(detail="Parent with this phone number does not exist.")
        return parent

    def get_queryset(self):
        return Guardian.objects.filter(merchant=self.request.merchant, role=PARENT)

    @extend_schema(
        description="""
**Retrieve the parent object if exist based on phone.**

### 🔐 Headers
- `Authorization`: Token your_auth_token *(Required)*

### 📄 Response
- Returns a object of parent data"""
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
