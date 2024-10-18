from django.db import models

from api.models.abstract.base import BaseModel


class Lookup(BaseModel):
    type = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_types",
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
