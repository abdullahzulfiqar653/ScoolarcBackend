import random

from django.db import models
from django.contrib.auth.models import User
from api.models.abstract.base import BaseModel


class Merchant(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="merchant"
    )
    code = models.CharField(max_length=4, unique=True, editable=False)
    domain = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = str(random.randint(1000, 9999))
                if not Merchant.objects.filter(code=code).exists():
                    self.code = code
                    break
        super().save(*args, **kwargs)

    class Meta:
        unique_together = [["name", "owner", "code"]]
