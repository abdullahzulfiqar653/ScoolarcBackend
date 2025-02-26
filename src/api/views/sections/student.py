from rest_framework.generics import ListCreateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers.student import StudentSerializer


class SectionListCreateStudentView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.section.students.all()