from django.db import models
from api.models.abstract.base import BaseModel


class Books(BaseModel):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    # TODO add foreignkey of class
    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        db_table = 'books'