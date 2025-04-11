from rest_framework.generics import ListCreateAPIView
from api.permissions import IsOutletMember, RolePermission
from api.serializers import StaffSerializer


class OutletListCreateStaffView(ListCreateAPIView):
    serializer_class = StaffSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.staff.all()