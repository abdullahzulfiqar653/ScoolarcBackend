from rest_framework.generics import ListAPIView
from api.models import Student, SectionStaffAndSubject
from api.serializers.parents_app import SectionBookTeacherSerializer


class SectionBookTeacherListAPIView(ListAPIView):
    pagination_class = None
    serializer_class = SectionBookTeacherSerializer

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        section_id = self.kwargs.get("section_id")

        return SectionStaffAndSubject.objects.filter(
            staff_section_id=section_id
        ).select_related("subject", "section_staff__user")
