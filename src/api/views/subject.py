from rest_framework.generics import UpdateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers.subject import SubjectSerializer


class SubjectUpdateAPIView(UpdateAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.subject.subject_class.class_subjects.all()
