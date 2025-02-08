from api.serializers.classes import ClassesSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember
from rest_framework.generics import  RetrieveUpdateDestroyAPIView


class ClassesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.classes.all()
