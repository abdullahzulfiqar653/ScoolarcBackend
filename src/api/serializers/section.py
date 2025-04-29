import secrets
from rest_framework import serializers

from api.models.section import Section
from .classes_minimal import ClassMinimalSerializer


class SectionSerializer(serializers.ModelSerializer):
    section_class = ClassMinimalSerializer(read_only=True)

    class Meta:
        model = Section
        fields = ("id", "name", "code", "section_class")
        read_only_fields = ("code",)

    def create(self, validated_data):
        book_ids = validated_data.pop("books_ids", [])

        validated_data["section_class"] = self.context["request"].classes
        section = Section.objects.create(**validated_data)
        # section.books_ids.set(book_ids)  # Now this works
        return section


class BulkSectionCreateSerializer(serializers.Serializer):
    sections = SectionSerializer(many=True, write_only=True)

    def validate_sections(self, value):
        names = [v.get("name") for v in value]
        if None in names:
            raise serializers.ValidationError("Each section must have a name.")
        if len(names) != len(set(names)):
            raise serializers.ValidationError(
                "Duplicate section names are not allowed."
            )
        return value

    def create(self, validated_data):
        request = self.context["request"]
        section_class = request.classes
        sections_data = validated_data["sections"]

        sections = [
            Section(
                id=f"{Section.UID_PREFIX}{secrets.token_hex(6)}",
                name=item["name"],
                section_class=section_class,
            )
            for item in sections_data
        ]
        Section.objects.bulk_create(sections)
        return sections

    def to_representation(self, instance):
        return {"message": "Sections created successfully.", "count": len(instance)}
