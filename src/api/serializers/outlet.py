from api.models.outlet import Outlet
from rest_framework import serializers


class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = ("id", "name", "province", "city", "location")

    def check_outlet_existance(self, outlet):
        if outlet:
            if self.instance:
                if not outlet.id == self.instance.id:
                    raise serializers.ValidationError("Outlet with this name already exist.")
            else:
                raise serializers.ValidationError("Outlet with this name already exist.")

    def validate_name(self, name):
        outlet = self.context.get("request").merchant.outlets.filter(name=name).first()
        self.check_outlet_existance(outlet)
        return name

    def create(self, validated_data):
        merchant = self.context.get("request").merchant
        validated_data["merchant"] = merchant

        merchant_member = merchant.members.first()
        outlet = super().create(validated_data)
        merchant_member.outlets.add(outlet)
        merchant_member.save()
        return outlet
