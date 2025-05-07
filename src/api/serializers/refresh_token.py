from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    member_id = serializers.CharField()
