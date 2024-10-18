import os

from django.apps import apps
from django.dispatch import receiver
from django.core.management import call_command
from django.db.models.signals import post_migrate, post_save

from api.models.lookup import Lookup
from api.models.merchant import Merchant
from api.models.merchant_member import MerchantMember


@receiver(post_migrate, sender=apps.get_app_config("api"))
def load_data_from_fixture(sender, **kwargs):
    lookups_data = os.path.join("api", "fixtures", "lookups.json")
    call_command("loaddata", lookups_data, app_label="api")


@receiver(post_save, sender=Merchant)
def create_merchant_member(sender, instance, created, **kwargs):
    if created:
        male = Lookup.objects.filter(name="Male").first()
        role = Lookup.objects.filter(name="Merchant").first()
        MerchantMember.objects.create(
            user=instance.owner, merchant=instance, role=role, gender=male
        )
