from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth.models import Permission, User
from api.models.merchant_member import MerchantMember


class PermissionSerializer(serializers.ModelSerializer):
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=MerchantMember.objects.none(), many=True, write_only=True
    )
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.none(), many=True, write_only=True
    )

    class Meta:
        model = Permission
        fields = [
            "id",
            "name",
            "codename",
            "member_ids",
            "content_type",
            "permission_ids",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            self.fields["member_ids"].queryset = request.merchant.members.all()
            self.fields["permission_ids"].queryset = request.user.user_permissions.all()

    def create(self, validated_data):
        user_role = self.context["request"].user.profile.role.name

        if user_role not in ["Merchant", "Principal"]:
            raise PermissionDenied("You do not have permission to perform this action.")

        members = validated_data["member_ids"]
        permissions = validated_data["permission_ids"]

        for member in members:
            role = member.user.profile.role.name
            if member.user.profile.role.name in ["Student", "Parent"]:
                raise PermissionDenied(
                    f"Permissions cannot be updated for the '{role}' with role."
                )
            permissions_to_set = member.user.user_permissions.all() | permissions
            member.user.user_permissions.set(permissions_to_set)
            # member.user.save()
        User.objects.bulk_update(
            [member.user for member in members],
            fields=["user_permissions"],
        )

        return validated_data
