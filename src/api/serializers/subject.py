import secrets
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


class BulkSubjectCreateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)

    def validate_subjects(self, value):
        titles = [v["title"] for v in value]
        if len(titles) != len(set(titles)):
            raise serializers.ValidationError("Duplicate titles are not allowed.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        subject_class = request.classes
        subjects_data = validated_data["subjects"]

        subjects = []
        for item in subjects_data:
            subjects.append(
                Subject(
                    code=Subject.get_unique_code(),
                    id=f"{Subject.UID_PREFIX}{secrets.token_hex(6)}",
                    title=item["title"],
                    subject_class=subject_class,
                )
            )
        Subject.objects.bulk_create(subjects)
        return subjects

    def to_representation(self, instance):
        return {"message": "Subjects created successfully.", "count": len(instance)}
