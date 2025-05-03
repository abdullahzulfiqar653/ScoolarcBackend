import random
from django.db import models
from api.models.abstract.base import BaseModel


class Subject(BaseModel):
    UID_PREFIX = 110

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True, blank=True)
    subject_class = models.ForeignKey(
        "api.Classes",
        on_delete=models.CASCADE,
        related_name="class_subjects",
        null=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding and not self.code:
            self.code = Subject.get_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def get_unique_code():
        while True:
            code = str(random.randint(1000, 9999))
            if not Subject.objects.filter(code=code).exists():
                return code

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
