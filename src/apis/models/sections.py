from django.db import models
from apis.models.abstract.base import BaseModel


class Sections(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    books = models.ManyToManyField("apis.Subject", related_name="sections")
    section_class = models.ForeignKey(
        "apis.Classes", on_delete=models.CASCADE, related_name="sections"
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [["name", "section_class"]]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        db_table = "sections"
        verbose_name = "Section"
