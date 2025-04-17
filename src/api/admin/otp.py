from django.contrib import admin
from api.models.otp import OTP


class OTPAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "name",
        "password",
        "is_used",
        "updated_at",
    )
    search_fields = (
        "code",
        "member__phone",
        "member__user__first_name",
    )  # You can adjust this based on your model relationships
    list_filter = ("is_used",)
    readonly_fields = (
        "member",
        "code",
        "is_used",
        "updated_at",
    )  # Add any fields that you want to be read-only

    def name(self, obj):
        return obj.member.user.first_name

    def phone(self, obj):
        return obj.member.phone

    def password(self, obj):
        return obj.code

    def save_model(self, request, obj, form, change):
        """Override save_model if you need to add custom behavior when saving."""
        if not obj.code:
            obj.generate_otp()  # Generate OTP before saving if code is not already present
        super().save_model(request, obj, form, change)


admin.site.register(OTP, OTPAdmin)
