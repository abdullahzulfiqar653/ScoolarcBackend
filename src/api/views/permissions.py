from rest_framework.generics import ListAPIView
from django.contrib.auth.models import Permission
from api.serializers.permissions import PermissionSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember


class PermissionsListAPIView(ListAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        user = self.request.user
        user_permissions = user.user_permissions.all()
        group_permissions = Permission.objects.filter(group__user=user)
        all_permissions = user_permissions | group_permissions
        return all_permissions.distinct()
