from django.db import models
from api.models.member import Member
from api.models.section_staff_and_subject import SectionStaffAndSubject


class Staff(Member):
    section = models.ManyToManyField(
        "api.Section",
        related_name="staff_sections",
        through=SectionStaffAndSubject,
    )
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = "staff"
