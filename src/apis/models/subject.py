from django.db import models
from apis.models.abstract.base import BaseModel


class Subject(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    subject_class = models.ForeignKey(
        "apis.Classes",
        on_delete=models.CASCADE,
        related_name="class_subject",
        # TODO: why null is true? It should be false as all subjects will be linked to a class I think?
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
