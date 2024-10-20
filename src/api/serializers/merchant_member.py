import secrets
from rest_framework import serializers
from django.contrib.auth.models import User

from api.models.lookup import Lookup
from django.contrib.auth.models import Group
from api.models.merchant_member import MerchantMember

from api.serializers.user import UserSerializer
from django.core.exceptions import ValidationError
from api.serializers.outlet import OutletSerializer
from api.serializers.merchant import MerchantSerializer


class MerchantMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    merchant = MerchantSerializer(read_only=True)
    outlets = OutletSerializer(many=True, read_only=True)
    cnic = serializers.CharField(required=False, max_length=13, min_length=13)
    phone = serializers.CharField(required=False, max_length=10, min_length=10)
    emergency_contact = serializers.CharField(
        required=False, max_length=10, min_length=10
    )
    role = serializers.PrimaryKeyRelatedField(queryset=Lookup.objects.all())
    gender = serializers.PrimaryKeyRelatedField(queryset=Lookup.objects.all())
    phone_network = serializers.PrimaryKeyRelatedField(queryset=Lookup.objects.all())

    class Meta:
        model = MerchantMember
        fields = [
            "id",
            "user",
            "role",
            "cnic",
            "phone",
            "status",
            "avatar",
            "gender",
            "address",
            "outlets",
            "merchant",
            "blood_group",
            "is_verified",
            "phone_network",
            "date_of_birth",
            "emergency_contact",
            "registration_number",
            "emergency_contact_name",
        ]
        read_only_fields = ["id", "registration_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["role"].queryset = Lookup.objects.filter(type__name="Role").exclude(
            name="Merchant"
        )
        self.fields["gender"].queryset = Lookup.objects.filter(type__name="Gender")
        self.fields["phone_network"].queryset = Lookup.objects.filter(
            type__name="PhoneNetwork"
        )

    def validate_cnic(self, value):
        if not value:
            return None
        if not value.isdigit():
            raise serializers.ValidationError("Ensure this field has numbers only.")

        merchant = self.context["request"].merchant
        existing_member_query = merchant.members.filter(cnic=value)
        if self.instance:
            existing_member_query = existing_member_query.exclude(id=self.instance.id)

        if existing_member_query.exists():
            raise serializers.ValidationError(
                "This CNIC is already registered for other user."
            )

        return value

    def validate_phone(self, value):
        merchant = self.context["request"].merchant
        if not value.isdigit():
            raise serializers.ValidationError("Ensure this field has numbers only.")

        existing_phone_query = merchant.members.filter(phone=value)
        if self.instance:
            existing_phone_query = existing_phone_query.exclude(id=self.instance.id)

        if existing_phone_query.exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate_emergency_contact(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Ensure this field has numbers only.")

    def validate_role(self, value):
        user_role = self.context["request"].user.profile.role.name
        role_permissions = {
            "Merchant": ["Principal", "Registrar", "Teacher", "Student", "Parent"],
            "Principal": ["Principal", "Registrar", "Teacher", "Student", "Parent"],
            "Registrar": ["Registrar", "Teacher", "Student", "Parent"],
            "Teacher": [],
            "Student": [],
            "Parent": [],
        }

        if value.name not in role_permissions.get(user_role, []):
            raise ValidationError(
                f"Users with the role '{user_role}' are not allowed to create members with the role '{value.name}'."
            )

        return value

    def generate_unique_username(self):
        while True:
            username = secrets.token_hex(8)
            if not User.objects.filter(username=username).exists():
                return username

    def create(self, validated_data):
        merchant = self.context["request"].merchant
        outlet = self.context["request"].outlet
        validated_data["merchant"] = merchant
        user = validated_data.pop("user", {})

        role = validated_data.get("role")
        prefix_map = {"Student": "STD", "Parent": "PAR"}
        prefix = prefix_map.get(role.name, "EMP")

        member = (
            merchant.members.filter(role=role).order_by("registration_number").last()
        )
        last_number = int(member.registration_number[3:]) + 1 if member else 10000
        validated_data["registration_number"] = f"{prefix}{last_number}"

        user = User.objects.create_user(
            username=self.generate_unique_username(), **user
        )
        user.groups.add(Group.objects.get(name=role.name))

        validated_data["user"] = user
        merchant_member = MerchantMember.objects.create(**validated_data)
        merchant_member.outlets.add(outlet)

        return merchant_member
