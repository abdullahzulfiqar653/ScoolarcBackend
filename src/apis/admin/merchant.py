from django import forms
from django.contrib import admin
from apis.models.lookup import Lookup
from apis.models.merchant import Merchant
from apis.models.outlet import Outlet
from apis.models.member import Member

admin.site.register(Outlet)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter the Lookup choices for the role field (filtering by "Role" type)
        role_type = Lookup.objects.get(
            name="Role"
        )  # Assuming "Role" is the parent type
        self.fields["role"].queryset = Lookup.objects.filter(type=role_type)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = MemberForm


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    autocomplete_fields = ["owner"]
    search_fields = ["name", "short_name", "code", "domain"]
