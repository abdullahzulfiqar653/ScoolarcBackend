from django import forms
from django.contrib import admin
from api.models.lookup import Lookup
from api.models.merchant import Merchant
from api.models.outlet import Outlet
from api.models.member import Member
from api.models.guardian import Guardian


admin.site.register(Outlet)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "mobile_notification_token",
        "primary_phone",
        "email",
        "role",
    ]
    pass


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "mobile_notification_token",
        "primary_phone",
        "email",
        "role",
    ]


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    autocomplete_fields = ["owner"]
    search_fields = ["name", "short_name", "code", "domain"]
