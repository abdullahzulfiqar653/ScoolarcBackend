from rest_framework import serializers
from apis.models.merchant import Merchant


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["id", "name"]
