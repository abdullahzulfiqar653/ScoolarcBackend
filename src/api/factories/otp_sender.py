from api.senders.email_sender import EmailOTPSender
from api.senders.whatsapp_sender import WhatsAppOTPSender


class OTPSenderFactory:
    @staticmethod
    def get_sender(platform: str):
        if platform == "email":
            return EmailOTPSender()
        elif platform == "whatsapp":
            return WhatsAppOTPSender()
        else:
            raise ValueError(f"Unsupported platform: {platform}")
