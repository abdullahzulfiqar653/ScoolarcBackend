from api.models import Classes
from rest_framework import serializers
from api.serializers import OutletSerializer


class ClassesSerializer(serializers.ModelSerializer):
    """ This serializer is used to serialize the classes. """
    outlet = OutletSerializer(read_only=True)

    class Meta:
        model = Classes
        fields = [
            'id',
            'name',
            'outlet',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        return Classes.objects.create(**validated_data, outlet=self.context['request'].outlet)