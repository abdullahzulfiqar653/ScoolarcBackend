class ClassesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [isMerchantMember, IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.outlet.classes.all()