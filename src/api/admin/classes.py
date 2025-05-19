from django.contrib import admin
from api.models.classes import Classes  # Adjust import path if needed
from api.models.subject import Subject

admin.site.register(Subject)


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "outlet", "coordinator")
    list_filter = ("outlet", "coordinator")
    search_fields = ("name", "outlet__name", "coordinator__name")
    ordering = ("-created_at",)
