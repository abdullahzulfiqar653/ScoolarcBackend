from api.senders.sms_sender import SmsOTPSender
from api.senders.email_sender import EmailOTPSender
from api.common.contants import SMS, EMAIL, WHATSAPP
from api.senders.whatsapp_sender import WhatsAppOTPSender


class OTPSenderFactory:
    @staticmethod
    def get_sender(platform: str):
        if platform == EMAIL:
            return EmailOTPSender()
        elif platform == WHATSAPP:
            return WhatsAppOTPSender()
        elif platform == SMS:
            return SmsOTPSender()
        else:
            raise ValueError(f"Unsupported platform: {platform}")
