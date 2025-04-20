import secrets
from api.models.classes import Classes
from api.models.section import Section

from rest_framework import serializers
from api.serializers.section import SectionSerializer


class ClassesSerializer(serializers.ModelSerializer):
    class_sections = SectionSerializer(many=True)

    class Meta:
        model = Classes
        fields = (
            "id",
            "name",
            "class_sections",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        method = None
        view = self.context.get("view")
        request = self.context.get("request")
        swagger_fake_view = getattr(view, "swagger_fake_view", False)

        if request:
            method = request.method
        if method in ("PATCH", "PUT"):
            self.fields["class_sections"].read_only = True

    def validate_class_sections(self, value):

        if self.instance is None and not value:
            raise serializers.ValidationError("At least one section is required.")

        section_names = [section["name"] for section in value]
        duplicates = [
            name for name in set(section_names) if section_names.count(name) > 1
        ]
        if duplicates:
            raise serializers.ValidationError(
                f"Duplicate section names not allowed: {', '.join(duplicates)}"
            )

        return value
    
    def validate_name(self, value):
        request = self.context.get("request")
        queryset = request.outlet.outlet_classes.filter(name=value)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError("Class name already exists.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["outlet"] = request.outlet
        sections = validated_data.pop("class_sections")
        created_class = super().create(validated_data)
        sections_data = []
        for section in sections:
            sections_data.append(
                Section(
                    id=f"{Section.UID_PREFIX}{secrets.token_hex(6)}",
                    name=section["name"],
                    section_class=created_class,
                )
            )
        Section.objects.bulk_create(sections_data)
        return created_class
