from rest_framework import serializers
from api.models import Member


class MemberNotificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["mobile_notification_token"]

    def create(self, validated_data):
        user = self.context["request"].user
        member = user.profile  # Assuming `user.profile` is the related Member instance

        # Only update mobile_notification_token
        member.mobile_notification_token = validated_data.get(
            "mobile_notification_token"
        )
        member.save(update_fields=["mobile_notification_token"])
        return member
