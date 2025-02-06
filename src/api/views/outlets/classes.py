from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.serializers import ClassesSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember


class ClassesListCreateView(ListCreateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.classes.all()

class ClassesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.classes.all()

