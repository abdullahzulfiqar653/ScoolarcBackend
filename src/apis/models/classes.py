from django.db import models
from apis.models.abstract.base import BaseModel


class Classes(BaseModel):
    name = models.CharField(max_length=255)
    outlet = models.ForeignKey(
        "apis.Outlet", on_delete=models.CASCADE, related_name="outlet_classes", null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        db_table = "classes"
        verbose_name = "Class"
