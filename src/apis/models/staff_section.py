from django.db import models
from apis.models.abstract.base import BaseModel


class StaffSection(BaseModel):
    staff = models.ForeignKey(
        "apis.Staff",
        on_delete=models.CASCADE,
        related_name="staff_sections",
    )
    section = models.ForeignKey(
        "apis.Sections",
        on_delete=models.CASCADE,
        related_name="section_staff",
    )
    is_head = models.BooleanField(default=False)
    # TODO I think one more boolean field is required to check if the staff is a class attendence taker or not
    # like is_head means he is coordinator of the section but is_attendence_taker means he is responsible for taking attendence of the class

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
