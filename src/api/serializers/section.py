from rest_framework import serializers

from api.models.section import Section
from api.models.classes import Classes


class ClassMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes  # import it at the top
        fields = ("id", "name")


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
