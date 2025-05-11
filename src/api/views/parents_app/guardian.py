from api.models.outlet import Outlet
from rest_framework.generics import ListAPIView

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
