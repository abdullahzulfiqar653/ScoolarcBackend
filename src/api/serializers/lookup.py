from rest_framework import serializers
from api.models.lookup import Lookup


class LookupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lookup
        fields = ["id", "name"]


class LookupOperationSerializer(serializers.ModelSerializer):
    sub_types = serializers.SerializerMethodField()

    class Meta:
        model = Lookup
        fields = ["id", "type", "name", "sub_types"]
        depth = 1

    def get_sub_types(self, obj):
        sub_types = obj.sub_types.all()
        return LookupSerializer(sub_types, many=True).data
