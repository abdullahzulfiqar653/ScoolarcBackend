from api.models.staff import Staff
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            "id",
            "cnic",
            "city",
            "area",
            "email",
            "bonus",
            "gender",
            "status",
            "avatar",
            "address",
            "country",
            "religion",
            "last_name",
            "first_name",
            "created_at",
            "blood_group",
            "basic_salary",
            "date_of_birth",
            "primary_phone",
            "emergency_contact",
            "emergency_contact_name",
        )
        read_only_fields = ("created_at",)
