from api.models.staff import Staff
from api.models.classes import Classes
from api.serializers.staff import StaffSerializer
from api.permissions import RolePermission, IsOutletMember
from api.serializers.classes_minimal import ClassMinimalSerializer
from api.serializers.classes_head_coordinator import ClassesHeadCoordinatorSerializer

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView


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


@extend_schema(
    methods=["GET"],
    description="""
Retrieve a list of classes for which the authenticated staff member is the head coordinator.

This endpoint returns a minimal representation of classes (ID and name only) coordinated by the current staff.

**Authorization:**  
Requires the user to be a member of the outlet and have a valid staff role.

**Response:**  
- 200 OK: A list of classes with fields: `id`, `name`.
""",
    responses={200: ClassMinimalSerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    description="""
Assign a list of classes to the authenticated staff member as head coordinator.

### 🔄 Behavior:
- This **replaces any existing coordinator assignments** of this staff member in the current outlet.
- Any previous classes where the staff was coordinator will have their coordinator cleared.
- New classes (passed via `classes`) will now have this staff as their coordinator.

**Fields:**

| Field   | Type    | Required | Notes                                                 |
|---------|---------|----------|-------------------------------------------------------|
| classes | list of IDs | ✅ Yes   | IDs of class records to assign to the staff         |

**Validation Notes:**
- All class IDs must belong to the current outlet.
- Only users with appropriate permissions can perform this action.

**Response:**
- 200 OK: Empty object `{}` on success.
- 400 Bad Request: On validation errors (e.g., invalid class IDs).
""",
    request=ClassesHeadCoordinatorSerializer,
    responses={
        200: OpenApiResponse(response={}, description="Coordinator assignments updated")
    },
)
class StaffClassesHeadCoordinatorListCreateAPIView(ListCreateAPIView):
    pagination_class = None
    queryset = Staff.objects.none()
    permission_classes = [IsOutletMember, RolePermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClassMinimalSerializer
        return ClassesHeadCoordinatorSerializer

    def list(self, request, *args, **kwargs):
        # Replace the queryset manually because we have to return classes coordinated by the staff
        # and not the classes of the outlet
        self.queryset = Classes.objects.filter(
            coordinator=request.staff, outlet=request.staff.outlets.first()
        )
        return super().list(request, *args, **kwargs)
