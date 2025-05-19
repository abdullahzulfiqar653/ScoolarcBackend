from datetime import date
from rest_framework import serializers
from api.models.attendance import Attendance


import requests
import json


def send_attendance_notification(status, token):
    url = "https://exp.host/--/api/v2/push/send"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {
        "to": token,
        "sound": "default",
        "title": "Attendance Update",
        "body": f"Your child has been marked {status}.",
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    if response.status_code != 200:
        print(f"Failed to send notification: {response.status_code} - {response.text}")
    else:
        print("Notification sent successfully")


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
            validated_data["student"] = student
        elif staff:
            lookup["staff"] = staff
            validated_data["staff"] = staff

        instance = Attendance.objects.filter(**lookup).first()
        if not instance:
            instance = Attendance.objects.create(**validated_data)

        else:
            if (date.today() - instance.created_at.date()).days > 3:
                raise serializers.ValidationError(
                    "Attendance cannot be updated after 3 days."
                )
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
        token = student.student_guardian.mobile_notification_token
        send_attendance_notification(validated_data["status"], token)
        return instance
