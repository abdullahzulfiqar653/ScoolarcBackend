from api.serializers.otp import OTPSerializer
from rest_framework.generics import CreateAPIView
from api.permissions import IsMerchantMemberAnonymous


class OTPView(CreateAPIView):
    serializer_class = OTPSerializer
    permission_classes = [IsMerchantMemberAnonymous]
