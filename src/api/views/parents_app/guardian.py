from rest_framework.generics import ListAPIView

from api.models.outlet import Outlet
from api.models.student import Student
from api.serializers import StudentSerializer
from api.serializers.parents_app import GuardianOutletSerializer


class GuardianOutletListView(ListAPIView):
    pagination_class = None
    serializer_class = GuardianOutletSerializer

    def get_queryset(self):
        guardian_id = self.kwargs["pk"]
        return (
            Outlet.objects.filter(
                outlet_classes__class_sections__section_students__student_guardian_id=guardian_id
            )
            .select_related("merchant")
            .distinct()
        )


class GuardianStudentListView(ListAPIView):
    pagination_class = None
    serializer_class = StudentSerializer

    def get_queryset(self):
        guardian_id = self.kwargs["guardian_id"]
        outlet_id = self.kwargs["outlet_id"]

        return Student.objects.filter(
            student_guardian_id=guardian_id,
            student_section__section_class__outlet_id=outlet_id,
        ).select_related("student_section__section_class")
