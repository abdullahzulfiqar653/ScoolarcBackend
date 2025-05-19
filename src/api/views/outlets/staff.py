from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from api.models.staff import Staff
from api.common.contants import STAFF_ROLES
from api.serializers.staff import StaffSerializer
from api.permissions import IsOutletMember, RolePermission


class OutletStaffListCreateAPIView(ListCreateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsOutletMember, RolePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "primary_phone", "email", "role"]

    def get_queryset(self):
        role = self.request.query_params.get("role")
        if self.request.method == "GET":
            if not role:
                raise ValidationError({"detail": "Role is required."})
            if role not in STAFF_ROLES:
                raise ValidationError(
                    {
                        "detail": f"Invalid role. Allowed roles are: {', '.join(STAFF_ROLES)}"
                    }
                )
            return Staff.objects.filter(outlets=self.request.outlet, role=role)
        return Staff.objects.none()

    @extend_schema(
        description="""
**Create a new staff member for the current outlet.**

### 🔐 Headers:
- `Authorization`: Token your_auth_token *(Required)*

### 📝 Required & Optional Fields:
| Field                  | Type    | Required | Notes                                                        |
|------------------------|---------|----------|--------------------------------------------------------------|
| role                   | string  | ✅ Yes   | Must be one of: `teacher`, `registrar`, `principal`.  |
| cnic                   | string  | ✅ Yes   | Must be 13 digits                                            |
| city                   | string  | ✅ Yes   |                                                              |
| area                   | string  | ✅ Yes   |                                                              |
| email                  | string  | ❌ No    | Must be valid email if provided                              |
| gender                 | string  | ✅ Yes   | `Male`, `Female`, or `Other`                                 |
| avatar                 | string  | ❌ No    | URL of the avatar image                                      |
| address                | string  | ❌ No    |                                                              |
| religion               | string  | ❌ No    | Must be one of: `islam`, `other`                             |
| last_name              | string  | ❌ No    |                                                              |
| first_name             | string  | ✅ Yes   |                                                              |
| date_of_birth          | string  | ❌ No    | Format: `YYYY-MM-DD`                                           |
| blood_group            | string  | ❌ No    | e.g. `A+`, `O-`, etc.                                            |
| primary_phone          | string  | ✅ Yes   | Must be exactly 10 digits, cannot start with 0               |
| emergency_contact      | string  | ❌ No    | Must be 10 digits if provided starting from 3                |
| emergency_contact_name | string  | ❌ No    |                                                              |
### ✅ Example Payload:
""",
        examples=[
            OpenApiExample(
                name="Create Staff Example",
                value={
                    "role": "teacher",
                    "cnic": "4210112345671",
                    "city": "Karachi",
                    "area": "DHA Phase 6",
                    "email": "teacher@example.com",
                    "gender": "Female",
                    "avatar": "https://cdn.example.com/teacher-avatar.png",
                    "address": "House 11, Lane 2",
                    "religion": "Islam",
                    "last_name": "Yousuf",
                    "first_name": "Maria",
                    "date_of_birth": "1990-06-15",
                    "blood_group": "A+",
                    "primary_phone": "3011234567",
                    "emergency_contact": "3007654321",
                    "emergency_contact_name": "Fatima",
                },
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        description="""
**Retrieve all staff members linked to the current outlet.**

### 🔐 Headers:
- `Authorization`: Token your_auth_token *(Required)*

### 🔎 Filters Supported:
- `search`: You can search using `first_name`, `last_name`, `primary_phone`, `email`, `area`, `address`.

### 📄 Response:
Returns a list of staff records.
""",
        parameters=[
            OpenApiParameter(
                name="role",
                required=True,
                type=str,
                description=f"Role of staff. Allowed: {', '.join(STAFF_ROLES)}",
                enum=STAFF_ROLES,  # 🎯 this makes dropdown automatically!
                location=OpenApiParameter.QUERY,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
