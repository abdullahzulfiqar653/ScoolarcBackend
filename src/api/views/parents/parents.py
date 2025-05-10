from api.common.contants import PARENT
from api.models.guardian import Guardian
from api.serializers.guardian import GuardianSerializer
from api.permissions import IsOutletMember, RolePermission

from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView


class ParentsRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = GuardianSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return Guardian.objects.filter(role=PARENT)

    @extend_schema(
        description="""
**Retrieve the parent object if exist based on id.**

### 🔐 Headers
- `Authorization`: Token your_auth_token *(Required)*

### 📄 Response
- Returns a object of parent data"""
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
