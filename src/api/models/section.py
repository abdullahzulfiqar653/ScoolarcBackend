from django.db import models
from api.models.abstract.base import BaseModel


class Section(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=24)
    coordinator = models.ForeignKey(
        "api.Staff",
        on_delete=models.CASCADE,
        related_name="coordinator_sections",
        null=True,
    )
    books = models.ManyToManyField(
        "api.Subject",
        related_name="books_sections",
    )
    section_class = models.ForeignKey(
        "api.Classes",
        on_delete=models.CASCADE,
        related_name="class_sections",
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [["name", "section_class"]]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        db_table = "sections"
