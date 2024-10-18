from rest_framework import generics
from api.serializers.outlet import OutletSerializer
from api.permissions import MerchantDomainPermission


class OutletListCreateView(generics.ListCreateAPIView):
    serializer_class = OutletSerializer
    permission_classes = [MerchantDomainPermission]

    def get_queryset(self):
        return self.request.user.member_profile.outlets.all()


class OutleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OutletSerializer
    permission_classes = [MerchantDomainPermission]

    def get_queryset(self):
        return self.request.user.member_profile.outlets.all()
