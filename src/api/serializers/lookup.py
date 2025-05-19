from typing import List
from api.models.lookup import Lookup
from rest_framework import serializers


class LookupNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookup
        fields = [
            "id",
            "name",
        ]


class LookupSerializer(serializers.ModelSerializer):
    sub_types = serializers.SerializerMethodField()

    class Meta:
        model = Lookup
        fields = [
            "id",
            "name",
            "type",
            "sub_types",
        ]

    def get_sub_types(self, obj) -> List[str]:
        return LookupNestedSerializer(obj.sub_types.all(), many=True).data
