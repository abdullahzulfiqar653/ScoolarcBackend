from django.db import models
from api.models.member import Member


class Student(Member):
    father_name = models.CharField(max_length=128)
    mother_name = models.CharField(max_length=128)
    father_cnic = models.CharField(max_length=13)
    b_form = models.FileField(upload_to="b_forms", null=True, blank=True)
    roll_number = models.CharField(max_length=24, unique=True, editable=False)
    student_section = models.ForeignKey(
        "api.Section",
        on_delete=models.CASCADE,
        related_name="section_students",
    )

    student_guardian = models.ForeignKey(
        "api.Guardian",
        on_delete=models.CASCADE,
        related_name="guardian_students",
    )

    def save(self, *args, **kwargs):
        if not self.roll_number:
            max_roll_number = self.__class__.objects.filter(
                section__section_class__outlet=self.student_section.section_class.outlet
            ).aggregate(max_roll=models.Max("roll_number"))["max_roll"]
            new_roll_number = int(max_roll_number or 0) + 1
            self.roll_number = f"{new_roll_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
