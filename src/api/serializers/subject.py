from api.models.subject import Subject
from rest_framework import serializers
from api.serializers.classes import ClassesSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """This serializer is used to serialize the subject."""
    subject_class = ClassesSerializer(read_only=True)
    class Meta:
        model = Subject
        fields = (
            "id",
            "code",
            'title',
            "created_at",
            "updated_at",
            "subject_class",
        )
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        validated_data["subject_class"] = self.context["request"].classes
        return super().create(validated_data)