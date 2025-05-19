from django.db import models
from api.models.abstract.base import BaseModel


class SectionStaffAndSubject(BaseModel):
    UID_PREFIX = 114
    section_staff = models.ForeignKey(
        "api.Staff",
        on_delete=models.CASCADE,
        related_name="staff_and_sections",
    )
    staff_section = models.ForeignKey(
        "api.Section",
        on_delete=models.CASCADE,
        related_name="section_and_staff",
    )
    subject = models.ForeignKey(
        "api.Subject",
        on_delete=models.CASCADE,
    )
    is_head = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
