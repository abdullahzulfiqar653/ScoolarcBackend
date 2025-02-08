from django.db import models
from api.models.abstract.base import BaseModel


class Subject(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    subject_class = models.ForeignKey(
        "api.Classes",
        on_delete=models.CASCADE,
        related_name="class_subject",
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
