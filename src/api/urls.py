from django.urls import path, include
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # =====================================================
    # Auth
    # =====================================================
    path("auth/", include("rest_framework.urls")),
    path("auth/token/", OTPView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # =====================================================
    # Permissions
    # =====================================================
    path("permissions/", PermissionsListAPIView.as_view(), name="permissions-list"),
    # =====================================================
    # Outllets
    # =====================================================
    path("outlets/", OutletListCreateView.as_view(), name="outlet-list-create"),
    path(
        "outlets/<str:pk>/",
        OutletRetrieveUpdateDestroyView.as_view(),
        name="outlet-retrieve-update-destroy",
    ),
    path(
        "outlets/<str:pk>/merchant-member",
        MerchantMemberListCreateView.as_view(),
        name="merchant-member-list-create",
    ),
]
