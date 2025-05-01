from django.db import models
from api.models.member import Member


class Guardian(Member):
    occupation = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name
