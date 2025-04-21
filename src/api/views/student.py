from api.models.student import Student
from api.serializers.student import StudentSerializer
from api.permissions import RolePermission, IsOutletMember

from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView


@extend_schema(
    methods=["GET"],
    description="Retrieve a student's complete profile by ID. Includes section, guardian, and outlet details.",
    responses={200: StudentSerializer},
)
@extend_schema(
    methods=["PUT", "PATCH"],
    description=(
        "Update a student's profile. "
        "`student_section` and `student_guardian` fields are not required in update requests."
    ),
    request=StudentSerializer,
    responses={200: StudentSerializer},
)
class StudentRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        outlet = self.request.student.student_section.section_class.outlet
        return Student.objects.filter(outlets=outlet).select_related(
            "student_section__section_class__outlet__merchant",
            "student_guardian",
        )
