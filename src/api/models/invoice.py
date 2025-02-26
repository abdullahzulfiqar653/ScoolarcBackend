from django.db import models
from api.models.abstract.base import BaseModel


INVOICE_STATUS = (
    ("PENDING", "Pending"),
    ("PAID", "Paid"),
    ("PARTIAL", "Partial"),
    ("OVERDUE", "Overdue"),
)


class Invoice(BaseModel):
    invoice_guardian = models.ForeignKey(
        "api.Guardian",
        on_delete=models.CASCADE,
        related_name="guardian_invoices",
    )
    students = models.ManyToManyField(
        "api.Student",
        related_name="student_invoices",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_status = models.CharField(
        max_length=255, choices=INVOICE_STATUS, default="PENDING"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    paid_date = models.DateTimeField(null=True, blank=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    mata_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.invoice_guardian.user.first_name + " " + self.invoice_guardian.user.last_name

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
