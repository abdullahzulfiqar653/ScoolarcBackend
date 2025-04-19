from api.serializers import ClassesSerializer
from api.permissions import RolePermission, IsOutletMember
from rest_framework.generics import ListCreateAPIView


class OutletClassesListCreateAPIView(ListCreateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.outlet_classes.all()
