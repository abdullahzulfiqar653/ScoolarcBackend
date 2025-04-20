from django.urls import path, include
from api.views import (
    OTPView,
    LookupListAPIView,
    ImagesCreateAPIView,
    RefreshTokenAPIView,
    PermissionsListAPIView,
    ClassListCreateSectionView,
    MerchantOutletListCreateView,
    ClassesRetrieveUpdateAPIView,
    OutletStudentListCreateAPIView,
    OutletClassesListCreateAPIView,
    OutletRetrieveUpdateDestroyView,
    SectionRetrieveUpdateDestroyView,
    StudentRetrieveUpdateDestroyView,
)

urlpatterns = [
    # =====================================================
    # Auth
    # =====================================================
    path("auth/", include("rest_framework.urls")),
    path("auth/token/", OTPView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path(
        "auth/image-upload/", ImagesCreateAPIView.as_view(), name="presigned-url"
    ),
    # =====================================================
    # Permissions
    # =====================================================
    path("permissions/", PermissionsListAPIView.as_view(), name="permissions-list"),
    # =====================================================
    # Outllets
    # =====================================================
    path("outlets/", MerchantOutletListCreateView.as_view(), name="outlet-list-create"),
    path(
        "outlets/<str:pk>/",
        OutletRetrieveUpdateDestroyView.as_view(),
        name="outlet-retrieve-update-destroy",
    ),
    # path(
    #     "outlets/<str:pk>/member",
    #     OutletMemberListCreateView.as_view(),
    #     name="merchant-member-list-create",
    # ),
    path(
        "outlets/<str:pk>/classes",
        OutletClassesListCreateAPIView.as_view(),
        name="merchant-classes-list-create",
    ),
    path(
        "outlets/<str:pk>/students",
        OutletStudentListCreateAPIView.as_view(),
        name="outlets-student-list-create",
    ),
    # =====================================================
    # Classes
    # =====================================================
    path(
        "classes/<str:pk>/",
        ClassesRetrieveUpdateAPIView.as_view(),
        name="classes-retrieve-update-destroy",
    ),
    path(
        "classes/<str:pk>/sections",
        ClassListCreateSectionView.as_view(),
        name="classes-section-list-create",
    ),
    # =====================================================
    # Sections
    # =====================================================
    path(
        "sections/<str:pk>/",
        SectionRetrieveUpdateDestroyView.as_view(),
        name="sections-retrieve-update-destroy",
    ),
    # =====================================================
    # Students
    # =====================================================
    path(
        "students/<str:pk>/",
        StudentRetrieveUpdateDestroyView.as_view(),
        name="students-retrieve-update-destroy",
    ),
    # =====================================================
    # Lookups
    # =====================================================
    path("lookup/<str:flag>/", LookupListAPIView.as_view(), name="lookup-list"),
]
