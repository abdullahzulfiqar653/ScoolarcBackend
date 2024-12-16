from django.contrib import admin
from api.models.lookup import Lookup


class LookupAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_type")  # Display fields
    search_fields = ["name"]  # Allows search by name in the admin
    autocomplete_fields = ["type"]  # Enables a search box for 'type' ForeignKey field

    def parent_type(self, obj):
        return (
            obj.type.name if obj.type else "No Parent"
        )  # Custom method to display parent type name


admin.site.register(Lookup, LookupAdmin)
