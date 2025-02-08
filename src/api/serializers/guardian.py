from api.models.guardian import Guardians
from rest_framework import serializers


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardians
        fields = (
            "id",
            "cnic",
            "phone",
            "avatar",
            "gender",
            "address",
            "occupation",
            "blood_group",
            "phone_network",
            "date_of_birth",
            "emergency_contact",
            "emergency_contact_name",
        )
        read_only_fields = (
            "role",
            "status",
            "created_at",
            "updated_at",
            "is_verified",
            "registration_number",
        )
        extra_kwargs = {"user": {"required": False}}
