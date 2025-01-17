from django.db import models
from api.models.abstract.base import BaseModel


class StaffAndSections(BaseModel):
    staff = models.ForeignKey(
        "api.Staff",
        on_delete=models.CASCADE,
        related_name="staff_sections",
    )
    section = models.ForeignKey(
        "api.Sections",
        on_delete=models.CASCADE,
        related_name="section_staff",
    )
    is_head = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
        ]