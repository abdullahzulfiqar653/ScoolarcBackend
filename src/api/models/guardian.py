from django.db import models
from api.models.member import Member


class Guardian(Member):
    occupation = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
