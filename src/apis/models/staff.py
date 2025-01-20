from django.db import models
from apis.models.member import Member


class Staff(Member):
    section = models.ManyToManyField(
        "apis.Sections", related_name="staff_sections", through="apis.StaffSection"
    )
    books = models.ManyToManyField(
        "apis.Subject",
        related_name="staff_books",
    )
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)

    # TODO: Add more fields like cv, experience, etc
    class Meta:
        db_table = "staff"
