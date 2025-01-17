from django.db import models
from api.models.abstract.base import BaseModel


class Sections(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    coordinator = models.ForeignKey(
        "api.Staff",
        on_delete=models.CASCADE,
        related_name="sections",
    )
    books = models.ManyToManyField(
        "api.Subject",
        related_name="sections",

    )
    section_class = models.ForeignKey(
        "api.Classes",
        on_delete=models.CASCADE,
        related_name="sections",
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [["name", "section_class"]]
        indexes = [
            models.Index(fields=['-created_at']),

        ]
        db_table = 'sections'