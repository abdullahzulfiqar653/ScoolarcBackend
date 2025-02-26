from api.models import Student, Guardian  # Import the correct Guardian model
from rest_framework import serializers
from api.serializers.section import SectionSerializer
from api.serializers.guardian import GuardianSerializer


class StudentSerializer(serializers.ModelSerializer):
    student_section = SectionSerializer(read_only=True)
    student_guardian = GuardianSerializer(read_only=True)
    guardian_id = serializers.PrimaryKeyRelatedField(
        queryset=Guardian.objects.all(), write_only=True, source="guardian"
    )

    class Meta:
        model = Student
        fields = [
            "father_name",
            "mother_name",
            "father_cnic",
            "b_form",
            "roll_number",
            "student_section",
            "student_guardian",
            "guardian_id",
        ]
        read_only_fields = ("created_at", "updated_at")


    def validate(self, data):
        """Perform multiple field validations at once."""
        father_cnic = data.get("father_cnic")
        b_form = data.get("b_form")

        # Validate father's CNIC
        if father_cnic and (not father_cnic.isdigit() or len(father_cnic) != 13):
            raise serializers.ValidationError({"father_cnic": "Father's CNIC must be a 13-digit number."})
        # Validate B-Form file (if provided)
        if b_form:
            allowed_types = ["application/pdf", "image/jpeg", "image/png"]
            max_size = 5 * 1024 * 1024  # 5MB

            if b_form.content_type not in allowed_types:
                raise serializers.ValidationError({"b_form": "Only PDF, JPEG, or PNG files are allowed."})
            if b_form.size > max_size:
                raise serializers.ValidationError({"b_form": "File size must not exceed 5MB."})

        return data

    def create(self, validated_data):
        """Custom create method to assign section and guardian correctly."""
        section = self.context.get("request").section
        student = Student.objects.create(**validated_data, section=section)
        return student
