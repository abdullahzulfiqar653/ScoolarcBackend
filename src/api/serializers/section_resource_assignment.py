import secrets
from rest_framework import serializers

from api.models.staff import Staff
from api.models.subject import Subject
from api.models.section import Section
from api.common.contants import TEACHER
from api.models.staff_and_section import StaffAndSection


class ClassSectionResourceAssignmentSerializer(serializers.Serializer):
    books = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True, write_only=True
    )
    teachers = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), many=True, write_only=True
    )
    coordinator = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), write_only=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "classes"):
            section_class = request.classes
            self.fields["books"].queryset = section_class.class_subjects.all()
            self.fields["teachers"].queryset = Staff.objects.filter(
                role=TEACHER, outlets=section_class.outlet
            )
            self.fields["coordinator"].queryset = self.fields["teachers"].queryset

    def validate(self, data):
        teacher_ids = data["teachers"]
        coordinator_id = data["coordinator"]

        if coordinator_id not in teacher_ids:
            raise serializers.ValidationError(
                {"coordinator": ["Coordinator must be one of the provided teachers."]}
            )
        return data

    def update(self, instance: Section, validated_data):
        # 1. Update books
        instance.books.set(validated_data["books"])

        # 2. Clear and re-add teacher assignments manually
        StaffAndSection.objects.filter(
            staff_section=instance
        ).hard_delete()  # Use hard_delete instead of delete

        staff_objs = validated_data["teachers"]
        for staff in staff_objs:
            StaffAndSection.objects.create(
                id=f"{StaffAndSection.UID_PREFIX}{secrets.token_hex(6)}",
                staff_section=instance,
                section_staff=staff,
                is_head=(staff == validated_data["coordinator"]),
            )

        # 3. Update coordinator at class level
        section_class = instance.section_class
        section_class.coordinator = validated_data["coordinator"]
        section_class.save()

        return instance


class ClassSectionResourceAssignmentRetrieveSerializer(serializers.Serializer):
    books = serializers.ListField(child=serializers.CharField())
    teachers = serializers.ListField(child=serializers.CharField())
    coordinator = serializers.CharField()

    def to_representation(self, instance):
        subjects = instance.books.values_list("id", flat=True)
        coordinator_id = instance.section_class.coordinator_id
        teachers = instance.staff_sections.values_list("id", flat=True)

        return {
            "books": list(subjects),
            "teachers": list(teachers),
            "coordinator": coordinator_id,
        }
