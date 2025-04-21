import re
import secrets
from rest_framework import serializers
from django.contrib.auth.models import User

from api.models.student import Student
from api.models.member import Member



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "city",
            "area",
            "role",
            "avatar",
            "gender",
            "b_form",
            "address",
            "last_name",
            "first_name",
            "blood_group",
            "father_name",
            "mother_name",
            "father_cnic",
            "roll_number",
            "date_of_birth",
            "student_section",
            "student_guardian",
        ]
        read_only_fields = ("created_at", "updated_at", "roll_number", "role")

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            from api.serializers.guardian import GuardianSerializer

            # Dynamically add write-only student_guardian field
            self.fields["student_guardian"] = GuardianSerializer()

    def create(self, validated_data):
        """Custom create method to assign section and guardian correctly."""
        from api.models.guardian import Guardian

        request = self.context.get("request")
        student_guardian = validated_data.pop("student_guardian", None)
        user = User.objects.create_user(
            username=student_guardian["primary_phone"],
            email=student_guardian.get("email", None),
            first_name=student_guardian["first_name"],
        )
        guardian = Guardian.objects.create(
            **student_guardian, user=user, merchant=request.merchant, role=Member.RoleChoices.PARENT
        )
        guardian.outlets.add(request.outlet)
        user = User.objects.create_user(
            username=f'{student_guardian["primary_phone"]}{secrets.token_hex(6)}',
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        validated_data["user"] = user
        validated_data["student_guardian"] = guardian
        validated_data["merchant"] = request.merchant
        validated_data["role"] = Member.RoleChoices.STUDENT
    
        student = super().create(validated_data)
        student.outlets.add(request.outlet)
        return student
