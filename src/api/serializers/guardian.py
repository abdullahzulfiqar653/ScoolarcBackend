import re
from api.models.guardian import Guardian

from rest_framework import serializers


class GuardianSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guardian
        fields = (
            "id",
            "city",
            "area",
            "cnic",
            "role",
            "email",
            "avatar",
            "gender",
            "address",
            "occupation",
            "first_name",
            "blood_group",
            "primary_phone",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "GET":
            from api.serializers.student import StudentSerializer

            # Dynamically add write-only student_guardian field
            self.fields["guardian_students"] = StudentSerializer(
                read_only=True, many=True
            )

    def validate_emergency_contact(self, value):
        if value:
            if not re.match(r"^\d{10}$", value):
                raise serializers.ValidationError(
                    "Primary phone must be exactly 10 digits long and numeric."
                )
            if value.strip().startswith("0"):
                raise serializers.ValidationError(
                    "Contact number cannot start with '0'."
                )
        return value

    def validate_cnic(self, value):
        if value and not re.match(r"^\d{13}$", value):
            raise serializers.ValidationError(
                "CNIC must be exactly 13 digits long and numeric."
            )
        return value

    def validate_primary_phone(self, value):
        merchant = self.context.get("request").merchant
        if not re.match(r"^\d{10}$", value):
            raise serializers.ValidationError(
                "Primary phone must be exactly 10 digits long and numeric."
            )
        if value.strip().startswith("0"):
            raise serializers.ValidationError("Contact number cannot start with '0'.")

        if self.instance:
            if value is None or self.instance.primary_phone == value:
                return self.instance.primary_phone

            queryset = merchant.members.filter(primary_phone=value)
            if queryset.exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "This phone number is already in use by another user."
                )
        else:
            queryset = merchant.members.filter(primary_phone=value)
            if queryset.exists():
                raise serializers.ValidationError(
                    "This phone number is already in use by another user."
                )
        return value
