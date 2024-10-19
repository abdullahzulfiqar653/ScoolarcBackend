from django.db import models
from django.db.models import Max

from api.models.abstract.base import BaseModel
from api.models.merchant import Merchant


class Outlet(BaseModel):
    name = models.CharField(max_length=255)
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="outlets"
    )
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    code = models.CharField(max_length=3, editable=False)

    def __str__(self) -> str:
        return f"{self.name} - {self.code}"

    def save(self, *args, **kwargs):
        if not self.code:
            last_code = Outlet.objects.filter(merchant=self.merchant).aggregate(
                Max("code")
            )["code__max"]
            self.code = f"{int(last_code) + 1}" if last_code else "100"
        super(Outlet, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("merchant", "code", "name")
        ordering = ["merchant", "code"]
