import json
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Assign or update permissions for Staff and Merchant groups"

    def handle(self, *args, **kwargs):
        permissions = Permission.objects.select_related('content_type').all()

        data = {}
        for perm in permissions:
            app_label = perm.content_type.app_label
            model = perm.content_type.model
            codename = f"{app_label}.{perm.codename}"
            
            key = f"{app_label}.{model}"
            if key not in data:
                data[key] = []
            data[key].append(codename)

        # Save to file
        with open("all_permissions.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Exported all permissions to all_permissions.json ✅")