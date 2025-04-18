import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from api.common.contants import ROLE_BASED_PERMISSIONS


class Command(BaseCommand):
    help = "Assign or update permissions for Staff and Merchant groups"

    def handle(self, *args, **kwargs):
        for group_name, perm_codenames in ROLE_BASED_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            permissions = []
            for codename in perm_codenames:
                try:
                    app_label, code = codename.split('.', 1)
                    perm = Permission.objects.get(content_type__app_label=app_label, codename=code)
                    permissions.append(perm)
                except Permission.DoesNotExist:
                    print(f"❌ Permission not found: {codename}")
            
            group.permissions.set(permissions)
            print(f"✅ Permissions set for group: {group_name}")
