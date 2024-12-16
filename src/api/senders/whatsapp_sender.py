from api.senders.base import OTPSender


class WhatsAppOTPSender(OTPSender):
    def send_otp(self, recipient: str, otp: str) -> None:
        # WhatsApp API integration logic
        print(f"WhatsApp OTP sent to {recipient}: {otp}")
