import os

from django.apps import apps
from django.dispatch import receiver
from django.core.management import call_command
from django.db.models.signals import post_migrate, post_save

from apis.models.lookup import Lookup
from apis.models.merchant import Merchant
from django.contrib.auth.models import Group
from apis.models.member import Member


@receiver(post_migrate, sender=apps.get_app_config("apis"))
def load_data_from_fixture(sender, **kwargs):
    lookups_data = os.path.join("apis", "fixtures", "lookups.json")
    groups_data = os.path.join("apis", "fixtures", "groups.json")
    call_command("loaddata", lookups_data, app_label="apis")
    call_command("loaddata", groups_data, app_label="auth")


@receiver(post_save, sender=Merchant)
def create_merchant_member(sender, instance, created, **kwargs):
    if created:
        role = Lookup.objects.filter(name="Merchant").first()
        instance.owner.groups.add(Group.objects.get(name=role.name))
        Member.objects.create(user=instance.owner, merchant=instance, role=role)
