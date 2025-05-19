from rest_framework import generics
from api.serializers.outlet import OutletSerializer
from api.permissions import isMerchantMember


class MerchantOutletListCreateView(generics.ListCreateAPIView):
    serializer_class = OutletSerializer
    permission_classes = [isMerchantMember]
    pagination_class = None
    
    def get_queryset(self):
        return self.request.user.profile.outlets.all()


class OutletRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    serializer_class = OutletSerializer
    permission_classes = [isMerchantMember]

    def get_queryset(self):
        return self.request.user.profile.outlets.all()
