from rest_framework.generics import CreateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers.section import BulkSectionCreateSerializer, SectionSerializer


class ClassSectionCreateAPIView(CreateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.class_sections.all()


class ClassSectionBulkCreateAPIView(CreateAPIView):
    serializer_class = BulkSectionCreateSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.class_sections.all()
