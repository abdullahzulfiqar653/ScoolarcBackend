from api.models.subject import Subject
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize the subject."""

    class Meta:
        model = Subject
        fields = ("id", "code", "title", "created_at", "updated_at")
        read_only_fields = ("code", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["subject_class"] = request.classes
        return super().create(validated_data)
