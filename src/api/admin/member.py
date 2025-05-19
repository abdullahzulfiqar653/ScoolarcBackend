from django.contrib import admin
from api.models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "role",
        "merchant",
        "status",
        "is_verified",
        "city",
        "area",
        "primary_phone",
    )
    list_filter = ("role", "status", "is_verified", "merchant", "city", "gender")
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "cnic",
        "primary_phone",
        "merchant__name",
    )
    autocomplete_fields = ("user", "merchant", "outlets")
    readonly_fields = ("is_staff",)
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user",
                    "merchant",
                    "outlets",
                    "role",
                    "is_verified",
                    "status",
                )
            },
        ),
        (
            "Personal Details",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "address",
                    "city",
                    "area",
                    "cnic",
                    "email",
                    "religion",
                    "blood_group",
                    "avatar",
                )
            },
        ),
        ("Emergency Info", {"fields": ("emergency_contact", "emergency_contact_name")}),
        (
            "Other",
            {
                "fields": (
                    "primary_phone",
                    "registration_number",
                    "mobile_notification_token",
                    "is_staff",
                )
            },
        ),
    )
