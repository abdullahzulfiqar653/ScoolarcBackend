import os
import json
import requests
from django.conf import settings

from api.models.member import Member
from api.senders.base import OTPSender


class SmsOTPSender(OTPSender):
    def send_otp(self, member: Member, otp: str) -> None:
        phone_number = member.primary_phone
        name = member.first_name
        message = json.dumps({"name": name, "pin": otp})
        api_url = (
            f"https://sendpk.com/api/sms.php?"
            f"api_key={settings.SMS_OTP_API_KEY}&sender=BrandName&mobile=92{phone_number}"
            f"&template_id=10052&message={message}&format=json"
        )
        response = requests.get(api_url)
        print(f"API URL: {api_url}")
        print(f"Response: {response.text}")
        return {
            "message": "OTP sent successfully!",
            "api_response": response.text,
        }
