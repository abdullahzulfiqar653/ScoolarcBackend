from rest_framework import generics
from api.serializers.outlet import OutletSerializer
from api.permissions import isMerchantMember


class OutletListCreateView(generics.ListCreateAPIView):
    serializer_class = OutletSerializer
    permission_classes = [isMerchantMember]

    def get_queryset(self):
        return self.request.user.profile.outlets.all()


class OutletRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OutletSerializer
    permission_classes = [isMerchantMember]

    def get_queryset(self):
        return self.request.user.profile.outlets.all()
