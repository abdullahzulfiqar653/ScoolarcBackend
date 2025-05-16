from datetime import datetime
from api.models.section import Section
from api.models.attendance import Attendance
from api.permissions import IsOutletMember, RolePermission

from api.serializers import (
    SectionSerializer,
    AttendanceSerializer,
    StudentMinimalSerializer,
)

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class SectionRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return Section.objects.filter(
            section_class__outlet=self.request.section.section_class.outlet,
        )


@extend_schema(
    summary="List students of a section",
    description="Returns a list of students in the current section",
    responses={200: StudentMinimalSerializer(many=True)},
)
class SectionStudentsListAPIView(ListAPIView):
    pagination_class = None
    serializer_class = StudentMinimalSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.section.section_students.all()


@extend_schema(
    summary="List student attendance for a section",
    description="Returns attendance records of students for a specific date within the section.",
    parameters=[
        OpenApiParameter(
            name="date",
            required=True,
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            description="Date for which to fetch attendance (format: YYYY-MM-DD)",
        )
    ],
    responses={200: AttendanceSerializer(many=True)},
)
class SectionAttendanceListAPIView(ListAPIView):
    pagination_class = None
    serializer_class = AttendanceSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        date_str = self.request.query_params.get("date")

        try:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Attendance.objects.none()

        return Attendance.objects.filter(
            student__student_section=self.request.section, created_at__date=query_date
        )
