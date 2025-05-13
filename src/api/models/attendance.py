from django.db import models
from api.models.staff import Staff
from api.models.student import Student
from api.models.abstract.base import BaseModel


class Status(models.TextChoices):
    PRESENT = "present", "Present"
    ABSENT = "absent", "Absent"
    LEAVE = "leave", "Leave"


class Attendance(BaseModel):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, related_name="attendances"
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, null=True, related_name="attendances"
    )
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "created_at"], name="unique_student_attendance"
            ),
            models.UniqueConstraint(
                fields=["staff", "created_at"], name="unique_staff_attendance"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{str(self.created_at)} - {self.status}"
