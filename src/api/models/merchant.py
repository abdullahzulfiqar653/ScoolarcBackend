from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User

from api.models.abstract.base import BaseModel


class Merchant(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="merchant"
    )
    short_name = models.CharField(max_length=7)
    code = models.CharField(max_length=4, unique=True, editable=False)
    domain = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            last_code = Merchant.objects.aggregate(Max("code"))["code__max"]
            self.code = f"{int(last_code) + 1}" if last_code else "1000"
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [["name", "owner", "code"]]
