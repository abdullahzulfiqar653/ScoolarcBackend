from api.models import Guardians
from rest_framework import serializers


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardians
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'user': {'required': False}
        }