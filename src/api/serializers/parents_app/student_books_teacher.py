from rest_framework import serializers
from api.models.section_staff_and_subject import SectionStaffAndSubject


class SectionBookTeacherSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="subject.name")
    teacher_name = serializers.CharField(source="section_staff.first_name")
    teacher_phone = serializers.CharField(source="section_staff.primary_phone")

    class Meta:
        model = SectionStaffAndSubject
        fields = ["book_name", "teacher_name", "teacher_phone"]
