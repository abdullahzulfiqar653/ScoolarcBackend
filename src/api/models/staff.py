from django.db import models
from api.models.member import Member


class Staff(Member):
    section = models.ManyToManyField(
        "api.Section", related_name="staff_sections", through="api.StaffAndSection"
    )
    books = models.ManyToManyField(
        "api.Subject",
        related_name="staff_books",
    )
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = "staff"
