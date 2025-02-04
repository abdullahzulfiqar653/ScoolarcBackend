from api.models import Sections
from rest_framework import serializers
from api.serializers import ClassesSerializer


class SectionsSerializer(serializers.ModelSerializer):
    section_class = ClassesSerializer(read_only=True)

    class Meta:
        model = Sections
        fields = [
            'id',
            'name',
            'code',
            'created_at',
            'updated_at',
            'section_class',

        ]
        read_only_fields = ('created_at', 'updated_at')
