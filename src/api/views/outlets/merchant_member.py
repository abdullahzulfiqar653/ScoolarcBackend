from rest_framework import generics
from api.serializers.merchant_member import MerchantMemberSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember


class MerchantMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = MerchantMemberSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.members.all()
