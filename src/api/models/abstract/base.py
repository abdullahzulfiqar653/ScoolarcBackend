from django.db import models

from api.models.mixins.uid import UIDMixin
from django_softdelete.models import SoftDeleteModel


class BaseModel(SoftDeleteModel, UIDMixin):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        permissions = [("can_undelete", "Can undelete this object")]

    def save(self, *args, **kwargs):
        self.set_uid()
        super().save(**kwargs)
