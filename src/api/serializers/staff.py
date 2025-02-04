from api.models import Staff
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True,source='user.first_name')
    last_name = serializers.CharField(required=True,source='user.last_name')
    class Meta:
        model = Staff
        fields = [
            'id',
            'bonus',
            'last_name',
            'first_name',
            'created_at',
            'updated_at',
            'basic_salary',
        ]
        read_only_fields = ('created_at', 'updated_at')