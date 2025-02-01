from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import OTP
from api.utils import generate_otp
from api.factories import OTPSenderFactory


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    platform = serializers.CharField(default="email", write_only=True)
    otp = serializers.CharField(max_length=6, required=False, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        otp_code = validated_data.get("otp")
        platform = validated_data.get("platform", "email")

        if otp_code:
            try:
                otp_record = request.member.otp
            except OTP.DoesNotExist:
                raise ValidationError({"otp": "Invalid OTP"})

            if otp_record.code != otp_code:
                raise ValidationError({"otp": "Invalid OTP"})

            if not otp_record.is_valid():
                raise ValidationError({"otp": "OTP expired"})

            refresh = RefreshToken.for_user(request.member.user)
            otp_record.is_used = True
            otp_record.save()
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        else:
            otp_record, _ = OTP.objects.get_or_create(member=request.member)
            otp_record.code = generate_otp()
            otp_record.is_used = False
            otp_record.save()
            sender = OTPSenderFactory.get_sender(platform)
            sender.send_otp(request.member, otp_record.code)

            return {"message": "OTP sent successfully!"}
