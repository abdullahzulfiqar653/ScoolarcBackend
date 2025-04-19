from api.serializers.classes import ClassesSerializer
from api.permissions import RolePermission, IsOutletMember

from rest_framework.generics import  RetrieveUpdateAPIView


class ClassesRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.outlet.outlet_classes.all()
