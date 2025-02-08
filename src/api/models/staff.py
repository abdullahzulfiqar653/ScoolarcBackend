from django.db import models
from api.models.member import Member


class Staff(Member):
    section = models.ManyToManyField(
        "api.Sections", related_name="staff_sections", through="api.StaffAndSections"
    )
    books = models.ManyToManyField(
        "api.Subject",
        related_name="staff_books",
    )
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "staff"
