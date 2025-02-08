from rest_framework import serializers
from api.models.section import Section
from api.models.subject import Subject
from api.serializers import StaffSerializer
from api.serializers import SubjectSerializer


class SectionSerializer(serializers.ModelSerializer):
    coordinator = StaffSerializer(read_only=True)
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
        books = validated_data.pop("books", [])
        section = Sections.objects.create(**validated_data)
        section.books.set(books)
        return section
