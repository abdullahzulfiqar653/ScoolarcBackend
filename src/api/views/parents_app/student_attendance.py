from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from api.models.attendance import Attendance
from api.filters.attendance import AttendanceFilter
from api.serializers.attendance import AttendanceSerializer


@extend_schema(
    summary="Get student's monthly attendance",
    description="Returns a list of attendance records for a given student. "
    "If 'month' is not provided, the current month is used. "
    "If 'year' is not provided, the current year is used.",
)
class StudentAttendanceListAPIView(ListAPIView):
    pagination_class = None
    filterset_class = AttendanceFilter
    filter_backends = (DjangoFilterBackend,)
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        student_id = self.kwargs.get("pk")
        return Attendance.objects.filter(student_id=student_id).order_by("-created_at")
