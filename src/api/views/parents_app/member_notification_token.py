from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.serializers import MemberNotificationTokenSerializer


class MemberNotificationTokenCreateAPIView(CreateAPIView):
    serializer_class = MemberNotificationTokenSerializer
