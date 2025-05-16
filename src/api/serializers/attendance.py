from datetime import date
from rest_framework import serializers
from api.models.attendance import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False, write_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "status", "reason", "created_at", "date", "student"]
        read_only_fields = ("student",)

    def create(self, validated_data):
        request = self.context.get("request")
        staff = getattr(request, "staff", None)
        student = getattr(request, "student", None)

        created_at__date = validated_data.pop("date", date.today())
        lookup = {"created_at__date": created_at__date}

        if student:
            lookup["student"] = student
        elif staff:
            lookup["staff"] = staff

        instance, created = Attendance.objects.get_or_create(
            defaults=validated_data,
            **lookup,
        )

        if not created:
            if (date.today() - instance.created_at.date()).days > 3:
                raise serializers.ValidationError(
                    "Attendance cannot be updated after 3 days."
                )

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        return instance
