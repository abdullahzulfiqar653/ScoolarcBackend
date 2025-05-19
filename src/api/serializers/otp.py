from datetime import timedelta
from django.utils.timezone import now

from rest_framework import serializers
from rest_framework.exceptions import Throttled
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import OTP
from api.utils import generate_otp
from api.factories import OTPSenderFactory
from api.common.contants import SMS, EMAIL, PARENT


class OTPSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    username = serializers.CharField(write_only=True)
    member_id = serializers.CharField(read_only=True)
    remaining_time = serializers.CharField(read_only=True)
    platform = serializers.CharField(default=SMS, write_only=True)
    otp = serializers.CharField(max_length=6, required=False, write_only=True)

    def create(self, validated_data):
        otp_code = validated_data.get("otp")
        request = self.context.get("request")
        platform = validated_data.get("platform", EMAIL)
        if getattr(request.member, "role", None) == PARENT:
            platform = SMS

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
            # otp_record.is_used = True
            # otp_record.save()
            return {
                "refresh": str(refresh),
                "member_id": request.member.id,
                "access": str(refresh.access_token),
            }

        else:
            otp_record, created = OTP.objects.get_or_create(member=request.member)
            if not created and otp_record.updated_at >= now() - timedelta(minutes=2):
                remaining_time = 120 - (now() - otp_record.updated_at).seconds
                raise Throttled(
                    detail=f"Please wait {remaining_time} seconds before trying again.",
                    wait=remaining_time,
                )

            otp_record.code = generate_otp()
            otp_record.is_used = False
            otp_record.save()
            sender = OTPSenderFactory.get_sender(platform)
            sender.send_otp(request.member, otp_record.code)

            return {"message": "OTP sent successfully!"}
