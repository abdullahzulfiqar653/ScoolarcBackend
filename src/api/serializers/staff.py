from api.models import Staff
from rest_framework import serializers
from api.serializers.user import UserSerializer


class StaffSerializer(serializers.ModelSerializer):
    profile = UserSerializer()

    class Meta:
        model = Staff
        fields = (
            "id",
            "bonus",
            "profile",
            "created_at",
            "updated_at",
            "basic_salary",
        )
        read_only_fields = ("created_at", "updated_at")
