from rest_framework import serializers
from api.models.section import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("id", "name", "code")
        read_only_fields = ("code", )

    def create(self, validated_data):
        book_ids = validated_data.pop("books_ids", [])

        validated_data["section_class"] = self.context["request"].classes
        section = Section.objects.create(**validated_data)
        # section.books_ids.set(book_ids)  # Now this works
        return section
