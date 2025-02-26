from rest_framework.generics import RetrieveUpdateDestroyAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers import SectionSerializer


class SectionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.sections.all()
