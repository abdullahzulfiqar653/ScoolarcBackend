from django.db import models
from api.models.abstract.base import BaseModel


class Section(BaseModel):
    UID_PREFIX = 108

    name = models.CharField(max_length=128)
    code = models.CharField(max_length=24)
    section_class = models.ForeignKey(
        "api.Classes",
        on_delete=models.CASCADE,
        related_name="class_sections",
        null=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together = [["name", "section_class"]]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        db_table = "sections"
