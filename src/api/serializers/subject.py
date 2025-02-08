from api.models.subject import Subject
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")
        extra_kwargs = {"service": {"required": False}}
