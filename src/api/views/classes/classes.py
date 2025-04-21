from api.serializers.classes import ClassesSerializer
from api.permissions import RolePermission, IsOutletMember

from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView


@extend_schema(
    methods=["GET"],
    description="Retrieve class details by ID, including its associated sections.",
    responses={200: ClassesSerializer},
)
@extend_schema(
    methods=["PUT", "PATCH"],
    description=(
        "Update class name only."
        "`class_sections` not required in update requests."
    ),
    request=ClassesSerializer,
    responses={200: ClassesSerializer},
)
class ClassesRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.outlet.outlet_classes.all()
