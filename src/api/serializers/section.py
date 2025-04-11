from api.models.subject import Subject
from rest_framework import serializers
from api.models.section import Section
from api.models.subject import Subject
from api.serializers.staff import StaffSerializer
from api.serializers.subject import SubjectSerializer
from api.serializers.classes import ClassesSerializer


class SectionSerializer(serializers.ModelSerializer):
    coordinator = StaffSerializer(read_only=True)
    section_class = ClassesSerializer(read_only=True)
    books = SubjectSerializer(many=True, read_only=True)
    books_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True, write_only=True, source="books"
    )

    class Meta:
        model = Section
        fields = (
            "id",
            "name",
            "code",
            "books",
            "books_ids",
            "coordinator",
            "section_class",
        )
        read_only_fields = ("created_at", "updated_at")
    def create(self, validated_data):
        book_ids = validated_data.pop("books_ids", [])

        validated_data["section_class"] = self.context["request"].classes
        section = Section.objects.create(**validated_data)
        # section.books_ids.set(book_ids)  # Now this works
        return section
