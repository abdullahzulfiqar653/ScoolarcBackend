from rest_framework.generics import ListCreateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers import SectionSerializer


class ClassListCreateSectionView(ListCreateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.class_sections.all()
