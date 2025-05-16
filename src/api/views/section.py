from api.models.section import Section
from api.serializers import SectionSerializer, StudentMinimalSerializer

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from api.permissions import IsOutletMember, RolePermission


class SectionRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return Section.objects.filter(
            section_class__outlet=self.request.section.section_class.outlet,
        )


class SectionStudentsListAPIView(ListAPIView):
    pagination_class = None
    serializer_class = StudentMinimalSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.section.section_students.all()
