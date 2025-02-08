from api.models import Student
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            "id",
        )
        read_only_fields = ("created_at", "updated_at")
