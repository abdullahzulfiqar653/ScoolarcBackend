# api/serializers/guardian.py

from rest_framework import serializers
from api.models import Outlet


class GuardianOutletSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source="merchant.name", read_only=True)

    class Meta:
        model = Outlet
        fields = ["id", "name", "merchant_name"]
