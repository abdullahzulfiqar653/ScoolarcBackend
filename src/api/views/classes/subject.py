from rest_framework.generics import ListCreateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers.subject import SubjectSerializer


class SubjectListCreateAPIView(ListCreateAPIView):
    pagination_class = None
    serializer_class = SubjectSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.class_subjects.all()
