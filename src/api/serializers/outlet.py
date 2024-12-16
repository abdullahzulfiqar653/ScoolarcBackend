from rest_framework import serializers
from api.models.outlet import Outlet


class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = ["id", "name", "province", "city", "location", "code"]
        read_only_fields = ["code"]

    def validate_name(self, name):
        outlet = self.context.get("request").merchant.outlets.filter(name=name)
        if not self.instance and outlet:
            raise serializers.ValidationError("Outlet with this name already exist.")
        return name

    def create(self, validated_data):
        merchant = self.context.get("request").merchant
        validated_data["merchant"] = merchant

        merchant_member = merchant.members.first()
        outlet = super().create(validated_data)
        merchant_member.outlets.add(outlet)
        merchant_member.save()
        return outlet
