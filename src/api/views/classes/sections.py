from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.permissions import IsOutletMember, RolePermission, InOutletOrMerchant
from api.serializers import SectionsSerializer


class ClassListCreateSectionView(ListCreateAPIView):
    serializer_class = SectionsSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.sections.all()



