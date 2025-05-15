from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from api.models.attendance import Attendance
from api.filters.attendance import AttendanceFilter
from api.serializers.attendance import AttendanceSerializer


@extend_schema(
    summary="Get student's monthly attendance",
    description="Returns a list of attendance records for a given student. "
    "If 'month' is not provided, the current month is used. "
    "Year is automatically taken as the current year.",
    parameters=[
        OpenApiParameter(
            name="month",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Month number (1-12). Optional. Defaults to current month.",
        )
    ],
    responses={200: AttendanceSerializer(many=True)},
)
class StudentAttendanceListAPIView(ListAPIView):
    pagination_class = None
    filterset_class = AttendanceFilter
    filter_backends = (DjangoFilterBackend,)
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        return Attendance.objects.filter(student_id=student_id).order_by("-created_at")
