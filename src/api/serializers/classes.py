from api.models.classes import Classes
from rest_framework import serializers
from api.serializers.outlet import OutletSerializer


class ClassesSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize the classes."""

    outlet = OutletSerializer(read_only=True)
    outlet_id = serializers.PrimaryKeyRelatedField(
        source="outlet",
        queryset=OutletSerializer.Meta.model.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Classes
        fields = ("id", "name", "outlet", "created_at", "updated_at", "outlet_id")
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        validated_data["outlet"] = self.context["request"].outlet
        return super().create(validated_data)
