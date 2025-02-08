class SectionRetrieveUpdateDestroySectionView(RetrieveUpdateDestroyAPIView):
    serializer_class = SectionsSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.sections.all()
