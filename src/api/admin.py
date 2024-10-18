from django import forms
from django.contrib import admin
from api.models.lookup import Lookup
from api.models.merchant import Merchant
from api.models.outlet import Outlet
from api.models.merchant_member import MerchantMember

admin.site.register(Lookup)
admin.site.register(Outlet)


# Register your models here.
class MerchantMemberForm(forms.ModelForm):
    class Meta:
        model = MerchantMember
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter the Lookup choices for the role field (filtering by "Role" type)
        role_type = Lookup.objects.get(
            name="Role"
        )  # Assuming "Role" is the parent type
        self.fields["role"].queryset = Lookup.objects.filter(type=role_type)


@admin.register(MerchantMember)
class MerchantMemberAdmin(admin.ModelAdmin):
    form = MerchantMemberForm


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    autocomplete_fields = ["owner"]
