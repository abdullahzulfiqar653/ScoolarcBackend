from enum import Enum
from django.db import models
from api.models.merchant import Merchant
from api.models.abstract.base import BaseModel


class ConfigType(Enum):
    EMAIL = ("email", "Email Configuration")
    BRANDING = ("branding", "Branding Configuration")
    OTP = ("otp", "OTP Configuration")
    NOTIFICATION = ("notification", "Notification Settings")
    OTHER = ("other", "Other Configuration")

    def __init__(self, key, description):
        self.key = key
        self.description = description

    @classmethod
    def choices(cls):
        """Return choices compatible with Django model fields."""
        return [(member.key, member.description) for member in cls]


class MerchantConfig(BaseModel):
    """
    Generic Merchant configuration model to handle key-value settings.
    """

    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="configs"
    )
    config_type = models.CharField(
        max_length=50,
        choices=ConfigType.choices(),
        help_text="Category of the configuration",
    )
    key = models.CharField(max_length=255, help_text="Configuration key")
    value = models.TextField(help_text="Configuration value")

    def __str__(self):
        return f"{self.merchant.name} - {self.config_type} - {self.key}"

    class Meta:
        unique_together = ["merchant", "config_type", "key"]
