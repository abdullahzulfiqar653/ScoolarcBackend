from django.db import models

from api.models.abstract.base import BaseModel
from api.models.merchant import Merchant


class Outlet(BaseModel):
    name = models.CharField(max_length=255)
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="outlets"
    )
    location = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = [["name", "merchant"]]
