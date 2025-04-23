from api.models.staff import Staff
from api.models.classes import Classes

from rest_framework import serializers


class ClassesHeadCoordinatorSerializer(serializers.Serializer):
    classes = serializers.PrimaryKeyRelatedField(
        queryset=Classes.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Classes
        fields = ("classes", "staff")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            outlet = request.staff.outlets.first()
            self.fields["classes"].queryset = outlet.outlet_classes.all()

    def get_outlet(self):
        """
        Helper method to retrieve the outlet from the context.
        """

    def create(self, validated_data):
        request = self.context.get("request")
        staff = request.staff
        outlet = request.staff.outlets.first()
        classes = validated_data.pop("classes", [])

        previous_classes = Classes.objects.filter(coordinator=staff, outlet=outlet)
        previous_classes.update(coordinator=None)

        for cls in classes:
            cls.coordinator = staff
        Classes.objects.bulk_update(classes, ["coordinator"])

        return {}
