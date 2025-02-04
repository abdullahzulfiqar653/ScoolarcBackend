from api.models import subjacts
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = subjacts
        fields = [
            'id',
            'name',
            'code',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'service': {'required': False}
        }