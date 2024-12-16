from api.models.merchant_config import MerchantConfig
from django.template.loader import render_to_string
from api.models.merchant_member import MerchantMember
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from api.senders.base import OTPSender


class EmailOTPSender(OTPSender):
    def send_otp(self, member: MerchantMember, otp: str) -> None:
        merchant = member.merchant
        email_configs = merchant.configs.filter(config_type="email")
        email_settings = {config.key: config.value for config in email_configs}
        from_email = email_settings.get("USER", settings.DEFAULT_EMAIL_USER)

        connection = get_connection(
            username=from_email,
            use_tls=email_settings.get("EMAIL_USE_TLS", "True") == "True",
            host=email_settings.get("EMAIL_HOST", settings.DEFAULT_EMAIL_HOST),
            port=int(email_settings.get("EMAIL_PORT", settings.DEFAULT_EMAIL_PORT)),
            password=email_settings.get("PASSWORD", settings.DEFAULT_EMAIL_PASSWORD),
        )

        subject = f"Your OTP code from {merchant.name}"
        html_message = render_to_string(
            "emails/otp_email.html",
            {
                "merchant_name": merchant.name,
                "otp": otp,
                "recipient_name": member.user.get_full_name(),
            },
        )

        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=f"{merchant.name} <{from_email}>",
            to=[member.user.email],
            connection=connection,
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
