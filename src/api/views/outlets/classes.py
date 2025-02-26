from rest_framework.generics import ListCreateAPIView
from api.serializers import ClassesSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember


class OutletClassesListCreateView(ListCreateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.classes.all()



