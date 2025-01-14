from django.db import models
from api.models.abstract.base import BaseModel


class Invoice(BaseModel):
    guardian = models.ForeignKey(
        "api.Guardians",
        on_delete=models.CASCADE,
        related_name="guardian_invoices",
    )
    students = models.ManyToManyField(
        "api.Student",
        related_name="student_invoices",
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.guardian.user.first_name + " " + self.guardian.user.last_name

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        db_table = 'invoices'