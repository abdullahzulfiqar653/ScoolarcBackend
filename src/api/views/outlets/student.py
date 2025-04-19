from rest_framework.generics import ListCreateAPIView

from api.permissions import IsOutletMember, RolePermission
from api.serializers.student import StudentSerializer
from api.models.student import Student


class OutletStudentListCreateAPIView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return Student.objects.filter(outlets=self.request.outlet)
