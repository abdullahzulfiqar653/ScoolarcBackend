from rest_framework import serializers
from api.models.classes import Classes


class ClassMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ("id", "name")
