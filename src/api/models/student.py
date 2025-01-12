from django.db import models
from api.models.merchant_member import MerchantMember


class Student(MerchantMember):
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=255, unique=True,editable=False)
    section = models.ForeignKey(
        "api.Sections",
        on_delete=models.CASCADE,
        related_name="student_section",
    )
    student_guardian = models.ForeignKey(
        "api.Guardian",
        on_delete=models.CASCADE,
        related_name="students_guardian",
    )

    def save(self, *args, **kwargs):
        self.roll_number = f"{self.section.code}-{str(self.id).zfill(4)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        db_table = 'students'

