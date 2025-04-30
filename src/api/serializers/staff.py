import re
from api.models.staff import Staff
from rest_framework import serializers
from api.common.contants import STAFF_ROLES


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            "id",
            "role",
            "cnic",
            "city",
            "area",
            "email",
            "gender",
            "status",
            "avatar",
            "address",
            "religion",
            "last_name",
            "first_name",
            "created_at",
            "blood_group",
            "date_of_birth",
            "primary_phone",
            "emergency_contact",
            "emergency_contact_name",
        )
        read_only_fields = ("created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.fields["status"].read_only = True

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
        if value and not re.match(r"^\d{10}$", value):
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

    def validate_role(self, value):
        print("teacher role", value)
        if value not in STAFF_ROLES:
            raise serializers.ValidationError(
                f"Invalid role. Allowed roles are: {', '.join(STAFF_ROLES)}"
            )
        return value

    def create(self, validated_data):
        validated_data.pop("status", None)
        request = self.context.get("request")
        validated_data["merchant"] = request.merchant
        staff = super().create(validated_data)
        staff.outlets.add(request.outlet)
        return staff
