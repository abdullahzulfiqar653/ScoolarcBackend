from django.urls import path
from api.views import (
    AppOtpView,
    AppRefreshTokenAPIView,
    GuardianOutletListView,
    GuardianStudentListView,
    StudentAttendanceListAPIView,
    SectionBookTeacherListAPIView,
    MemberNotificationTokenCreateAPIView,
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
        "section/<str:section_id>/books/",
        SectionBookTeacherListAPIView.as_view(),
        name="books-teacher-list",
    ),
    path(
        "student/<str:pk>/attendance/",
        StudentAttendanceListAPIView.as_view(),
        name="student-attendance-list",
    ),
    path(
        "parents/<str:pk>/outlets/<str:outlet_id>/students/",
        GuardianStudentListView.as_view(),
        name="guardian-student-list",
    ),
    path(
        "member-notification-token/",
        MemberNotificationTokenCreateAPIView.as_view(),
        name="update-notification-token",
    ),
]
