from django.db import models
from django.db.models import Q
from api.models.abstract.base import BaseModel


class Lookup(BaseModel):
    type = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_types",
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id} \t name: {self.name}"

    class Meta:
        unique_together = ("name", "type")

    @staticmethod
    def get_cities():
        """Retrieve all top-level cities (entries with no parent type)."""
        return Lookup.objects.filter(type__name="city")

    @staticmethod
    def get_areas_by_city(city):
        """Retrieve all areas for a specific city."""
        city = Lookup.objects.filter(
            Q(type__name="city") & (Q(name=city) | Q(id=city))
        ).first()
        return Lookup.objects.filter(type=city) if city else Lookup.objects.none()
