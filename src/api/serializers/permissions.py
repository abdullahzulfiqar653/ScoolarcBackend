from itertools import chain
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth.models import Permission
from api.models.member import Member
from api.common.contants import (
    ROLES_ALLOWED_TO_ASSIGN_PERMISSIONS,
    ROLES_NOT_ALLOWED_TO_HAVE_PERMISSIONS,
)


class PermissionSerializer(serializers.ModelSerializer):
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), many=True, write_only=True
    )
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "codename",
            "member_ids",
            "content_type",
            "permission_ids",
        )
        read_only_fields = ("name", "codename", "content_type")

    def get_member_queryset(self, request):
        return request.merchant.members.all()

    def get_permission_queryset(self, request):
        user = request.user
        direct_perms = user.user_permissions.all()
        group_perms = Permission.objects.filter(group__user=user)
        return (direct_perms | group_perms).distinct()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        # check to ignore swagger error
        if hasattr(request, "user") and request.user.is_authenticated:
            self.fields["member_ids"].queryset = self.get_member_queryset(request)
            self.fields["permission_ids"].queryset = self.get_permission_queryset(
                request
            )

    def create(self, validated_data):
        user_role = self.context["request"].user.profile.role

        if user_role not in ROLES_ALLOWED_TO_ASSIGN_PERMISSIONS:
            raise PermissionDenied("You do not have permission to perform this action.")

        members = validated_data["member_ids"]
        permissions = validated_data["permission_ids"]
        for member in members:
            role = member.user.profile.role
            if member.user.profile.role in ROLES_NOT_ALLOWED_TO_HAVE_PERMISSIONS:
                raise PermissionDenied(
                    f"Permissions cannot be updated for the '{role}' with role."
                )
            permissions_to_set = chain(member.user.user_permissions.all(), permissions)
            member.user.user_permissions.set(permissions_to_set)

        return validated_data
