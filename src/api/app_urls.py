from django.urls import path
from api.views import (
    AppOtpView,
    AppRefreshTokenAPIView,
    GuardianOutletListView,
    GuardianStudentListView,
)

urlpatterns = [
    path(
        "auth/token/",
        AppOtpView.as_view(),
        name="parents-otp-view",
    ),
    path("auth/token/refresh/", AppRefreshTokenAPIView.as_view(), name="token_refresh"),
    path(
        "guardian/<str:pk>/outlets/",
        GuardianOutletListView.as_view(),
        name="guardian-outlet-list",
    ),
    path(
        "parents/<str:guardian_id>/outlets/<str:outlet_id>/students/",
        GuardianStudentListView.as_view(),
        name="guardian-student-list",
    ),
]
