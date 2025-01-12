from django.db import models
from api.models.merchant_member import MerchantMember


class Guardian(MerchantMember):
    occupation = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        db_table = 'guardians'
