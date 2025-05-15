from api.models.student import Student
from api.serializers.student import StudentSerializer
from api.serializers.attendance import AttendanceSerializer

from api.filters.attendance import AttendanceFilter
from api.permissions import RolePermission, IsOutletMember

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView


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


@extend_schema(
    methods=["GET"],
    description="List attendance records for a student. You can filter by `created_at_year` and `created_at_month`.",
    parameters=[
        OpenApiParameter(
            name="created_at_year",
            required=False,
            type=int,
            location="query",
            description="Filter by attendance year (e.g., 2025)",
        ),
        OpenApiParameter(
            name="created_at_month",
            required=False,
            type=int,
            location="query",
            description="Filter by attendance month (1-12)",
        ),
    ],
    responses={200: AttendanceSerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    description="Create or update today's attendance for a student. Automatically updates if the record for today already exists.",
    request=AttendanceSerializer,
    responses={200: AttendanceSerializer},
)
class StudentAttendanceListCreateAPIView(ListCreateAPIView):
    pagination_class = None
    filterset_class = AttendanceFilter
    serializer_class = AttendanceSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.student.attendances.all()
