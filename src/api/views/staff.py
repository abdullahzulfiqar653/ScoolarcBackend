from api.models.staff import Staff
from api.serializers.staff import StaffSerializer
from api.permissions import RolePermission, IsOutletMember
from api.serializers.classes_head_coordinator import ClassesHeadCoordinatorSerializer

from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView


@extend_schema(
    methods=["GET"],
    description="""
Retrieve a staff member's complete profile by ID.  
Includes staff's section(s), outlet(s), and other relevant details.
""",
    responses={200: StaffSerializer},
)
@extend_schema(
    methods=["PUT", "PATCH"],
    description="""
Update a staff member's profile by ID.

You can modify any of the following fields:

| Field                 | Type     | Required | Notes                                                                 |
|----------------------|----------|----------|-----------------------------------------------------------------------|
| role                 | string   | ✅ Yes   | Must be one of: `teacher`, `admin`, `principal`, etc. (`STAFF_ROLES`)|
| cnic                 | string   | ✅ Yes   | 13-digit numeric value only                                           |
| city                 | string   | ✅ Yes   | Cannot be blank                                                       |
| area                 | string   | ✅ Yes   | Cannot be blank                                                       |
| email                | string   | ❌ No    | Must be a valid email format if provided                              |
| gender               | string   | ✅ Yes   | `Male`, `Female`, or `Other` 
| status               | bool     | ❌ No    | `true` or `false`                                         |
| avatar               | string   | ❌ No    | Image URL (can be null)                                               |
| address              | string   | ✅ Yes   | Cannot be blank                                                       |
| religion             | string   | ❌ No    | Optional, but if present cannot be blank                              |
| last_name            | string   | ❌ No    | Optional                                                              |
| first_name           | string   | ✅ Yes   | Cannot be blank                                                       |
| blood_group          | string   | ❌ No    | `A+`, `B+`, etc. (optional)                                           |
| date_of_birth        | string   | ✅ Yes   | Format: `YYYY-MM-DD`                                                  |
| primary_phone        | string   | ✅ Yes   | 10-digit numeric (must not start with 0)                              |
| emergency_contact    | string   | ❌ No    | 10-digit numeric (must not start with 0)                              |
| emergency_contact_name | string | ❌ No    | Optional                                                              |

### 🧠 Validation Notes:
- All numeric fields like `cnic` or phone must follow strict digit count and no starting 0.
- If you try to update the `primary_phone` to one already used by another member, it will raise a validation error.

**Response:**
- Returns the updated staff profile on success.
- Returns detailed field-level errors on failure.
""",
    request=StaffSerializer,
    responses={200: StaffSerializer},
)
class StaffRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        # You probably want to filter by outlet, depending on current user's outlet context
        # Assuming `request.outlet` is set by middleware (as in your previous code)
        return Staff.objects.filter(outlets=self.request.staff.outlets.first())


class StaffClassesHeadCoordinatorCreateAPIView(CreateAPIView):
    queryset = Staff.objects.none()
    serializer_class = ClassesHeadCoordinatorSerializer
    permission_classes = [IsOutletMember, RolePermission]
