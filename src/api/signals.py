import os

from django.apps import apps
from django.dispatch import receiver
from django.core.management import call_command
from django.db.models.signals import post_migrate, post_save

from api.models.staff import Staff
from api.common.contants import MERCHANT
from api.models.merchant import Merchant
from django.contrib.auth.models import Group


# @receiver(post_migrate, sender=apps.get_app_config("api"))
# def load_data_from_fixture(sender, **kwargs):
#     lookups_data = os.path.join("api", "fixtures", "lookups.json")
#     groups_data = os.path.join("api", "fixtures", "groups.json")
#     call_command("loaddata", lookups_data, app_label="api")
#     call_command("loaddata", groups_data, app_label="auth")


@receiver(post_save, sender=Merchant)
def create_merchant_member(sender, instance, created, **kwargs):
    if created:
        obj, _ = Group.objects.get_or_create(name="merchant")
        instance.owner.groups.add(obj)
        Staff.objects.create(user=instance.owner, merchant=instance, role=MERCHANT)
