from datetime import datetime
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from api.models.attendance import Attendance
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
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        today = datetime.today()
        current_year = today.year

        try:
            month = int(self.request.query_params.get("month", today.month))
        except ValueError:
            month = today.month  # fallback silently or raise error if desired

        return Attendance.objects.filter(
            student_id=student_id,
            created_at__month=month,
            created_at__year=current_year,
        ).order_by("-created_at")
