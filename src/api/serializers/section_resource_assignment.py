import secrets
from rest_framework import serializers

from api.models.staff import Staff
from api.models.subject import Subject
from api.models.section import Section
from api.common.contants import TEACHER
from api.models.section_staff_and_subject import SectionStaffAndSubject


class TeacherBookSerializer(serializers.Serializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.none())
    book = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        context = self.context
        if context.get("teacher_queryset"):
            self.fields["teacher"].queryset = context["teacher_queryset"]
        if context.get("subject_queryset"):
            self.fields["book"].queryset = context["subject_queryset"]


class ClassSectionResourceAssignmentSerializer(serializers.Serializer):
    section_teacher_and_subject = TeacherBookSerializer(many=True, write_only=True)
    coordinator = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.none(),
        write_only=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "classes"):
            section_class = request.classes
            teacher_qs = Staff.objects.filter(
                role=TEACHER, outlets=section_class.outlet
            )
            subject_qs = section_class.class_subjects.all()

            self.fields["coordinator"].queryset = teacher_qs

            if request.method in ("PUT", "PATCH"):
                # Pass to child serializer via context
                self.fields["section_teacher_and_subject"] = TeacherBookSerializer(
                    many=True,
                    context={
                        **self.context,
                        "teacher_queryset": teacher_qs,
                        "subject_queryset": subject_qs,
                    },
                    write_only=True,
                )

    def validate(self, data):
        coordinator = data["coordinator"]
        teachers = [entry["teacher"] for entry in data["section_teacher_and_subject"]]
        if coordinator not in teachers:
            raise serializers.ValidationError(
                {"coordinator": "Coordinator must be one of the provided teachers."}
            )
        return data

    def update(self, instance: Section, validated_data):
        # 1. Clear previous assignments
        SectionStaffAndSubject.objects.filter(staff_section=instance).hard_delete()
        entries = validated_data["section_teacher_and_subject"]
        coordinator = validated_data["coordinator"]

        new_links = [
            SectionStaffAndSubject(
                id=f"{SectionStaffAndSubject.UID_PREFIX}{secrets.token_hex(6)}",
                staff_section=instance,
                section_staff=entry["teacher"],
                subject=entry["book"],
                is_head=(entry["teacher"] == coordinator),
            )
            for entry in entries
        ]
        SectionStaffAndSubject.objects.bulk_create(new_links)

        # 2. Update coordinator at class level
        section_class = instance.section_class
        section_class.coordinator = coordinator
        section_class.save()

        return instance


class SectionTeacherSubjectPairSerializer(serializers.Serializer):
    teacher = serializers.CharField()
    book = serializers.CharField()


class ClassSectionResourceAssignmentRetrieveSerializer(serializers.Serializer):
    section_teacher_and_subject = SectionTeacherSubjectPairSerializer(many=True)
    coordinator = serializers.CharField()

    def to_representation(self, instance):
        # Fetch teacher-book pairs from the through model
        assignments = SectionStaffAndSubject.objects.filter(staff_section=instance)
        section_teacher_and_subject = [
            {
                "teacher": str(assignment.section_staff_id),
                "book": str(assignment.subject_id),
            }
            for assignment in assignments
        ]

        return {
            "section_teacher_and_subject": section_teacher_and_subject,
            "coordinator": str(instance.section_class.coordinator_id),
        }
