from rest_framework.generics import ListCreateAPIView, CreateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers.subject import SubjectSerializer, BulkSubjectCreateSerializer


class ClassSubjectListCreateAPIView(ListCreateAPIView):
    pagination_class = None
    serializer_class = SubjectSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.class_subjects.all()


class ClassSubjectBulkCreateAPIView(CreateAPIView):
    serializer_class = BulkSubjectCreateSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.class_subjects.all()
