from rest_framework import generics

from api.models.lookup import Lookup
from api.serializers.lookup import LookupSerializer
from drf_spectacular.utils import extend_schema


class LookupListAPIView(generics.ListAPIView):
    serializer_class = LookupSerializer
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        flag = self.kwargs["flag"]
        return Lookup.objects.filter(type__name=flag).prefetch_related("sub_types")

    @extend_schema(
        description="""
### **Handles Lookup Information Retrieval**

This API is used to fetch lookup information based on the `flag` parameter.

---

#### **🟢 Request Parameters (Path)**
| Parameter |  Required | Description |
|-----------|-----------|-------------|
| `flag`    | ✅ Yes   | The lookup type (e.g., `city`, `keys`) |

**Accepted Flags:**
- `city` → Returns a list of cities and their sub-areas.\n
- `keys` → Returns metadata keys for user suggestions.

""",
        responses={200: LookupSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
