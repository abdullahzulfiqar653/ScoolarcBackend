from rest_framework import generics
from api.serializers.member import MemberSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember


class MemberListCreateView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.members.all()

