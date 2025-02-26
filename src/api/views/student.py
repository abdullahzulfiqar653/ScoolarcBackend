from rest_framework.generics import  RetrieveUpdateDestroyAPIView
from api.serializers.student import StudentSerializer
from api.permissions import isMerchantMember, RolePermission, IsOutletMember


class StudentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.section.students.all()