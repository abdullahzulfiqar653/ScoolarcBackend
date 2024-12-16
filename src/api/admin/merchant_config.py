from django.contrib import admin
from api.models.merchant_config import MerchantConfig


@admin.register(MerchantConfig)
class MerchantConfigAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MerchantConfig model.
    """

    list_display = (
        "merchant",
        "config_type",
        "key",
        "value",
        "created_at",
        "updated_at",
    )
    list_filter = ("config_type", "merchant")
    search_fields = ("merchant__name", "key", "value")
    ordering = ("merchant", "config_type", "key")
    autocomplete_fields = ["merchant"]
    fieldsets = (
        (
            "Configuration Details",
            {
                "fields": (
                    "merchant",
                    "config_type",
                    "key",
                    "value",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")


class MerchantConfigInline(admin.TabularInline):
    model = MerchantConfig
    extra = 1
