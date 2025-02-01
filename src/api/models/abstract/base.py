from django.db import models

from api.models.mixins.uid import UIDMixin
from django_softdelete.models import SoftDeleteModel


class BaseModel(SoftDeleteModel, UIDMixin):
    id = models.CharField(max_length=15, primary_key=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    restored_at = models.DateTimeField(blank=True, null=True, editable=False)
    transaction_id = models.UUIDField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True
        permissions = [("can_undelete", "Can undelete this object")]

    def save(self, *args, **kwargs):
        self.set_uid()
        super().save(**kwargs)
