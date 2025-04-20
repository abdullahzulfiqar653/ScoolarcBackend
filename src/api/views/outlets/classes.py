from api.serializers import ClassesSerializer
from api.permissions import RolePermission, IsOutletMember

from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiExample

class OutletClassesListCreateAPIView(ListCreateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.outlet_classes.all()

    @extend_schema(
        description="""**Retrieve all classes for the current outlet.**
**Headers:**
- Authorization: Token your_auth_token *(Required)*

**Response:**
- List of classes with their associated sections.
        """
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
    description="""Create a new class and attach at least one section. \n
**Validation:**
    - `name` must be unique per outlet.
    - `class_sections` must have at least one section with unique names.

**Headers:**
    - Authorization: Token your_auth_token *(Required)*

**Request Body:**
    - `name`: string (required)
    - `class_sections`: array of section objects (required, at least one)

**Section object:**
    - `name`: string (required)

**Response:**
    - Created class object with list of created sections.
        """,
        examples=[
            OpenApiExample(
                "Example Class Create",
                value={
                    "name": "Class 10",
                    "class_sections": [
                        {"name": "Red"},
                        {"name": "Green"}
                    ]
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
