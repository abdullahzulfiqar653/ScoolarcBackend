from django.urls import path, include
from api.views import (
    OTPView,
    LookupListAPIView,
    ImagesCreateAPIView,
    RefreshTokenAPIView,
    PermissionsListAPIView,
    OutletParentsListAPIView,
    StaffRetrieveUpdateAPIView,
    OutletParentsRetrieveAPIView,
    MerchantOutletListCreateView,
    ClassesRetrieveUpdateAPIView,
    SectionRetrieveUpdateAPIView,
    StudentRetrieveUpdateAPIView,
    OutletStaffListCreateAPIView,
    OutletStudentListCreateAPIView,
    OutletClassesListCreateAPIView,
    OutletRetrieveUpdateDestroyView,
    StaffClassesHeadCoordinatorCreateAPIView,
)

urlpatterns = [
    # =====================================================
    # Auth
    # =====================================================
    path("auth/", include("rest_framework.urls")),
    path("auth/token/", OTPView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("auth/image-upload/", ImagesCreateAPIView.as_view(), name="presigned-url"),
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
    path(
        "outlets/<str:outlet_id>/classes",
        OutletClassesListCreateAPIView.as_view(),
        name="merchant-classes-list-create",
    ),
    path(
        "outlets/<str:outlet_id>/students",
        OutletStudentListCreateAPIView.as_view(),
        name="outlets-student-list-create",
    ),
    path(
        "outlets/<str:outlet_id>/staff",
        OutletStaffListCreateAPIView.as_view(),
        name="outlets-student-list-create",
    ),
    path(
        "outlets/<str:outlet_id>/parents",
        OutletParentsListAPIView.as_view(),
        name="outlets-parents-list",
    ),
    path(
        "outlets/<str:outlet_id>/parents/<str:phone>/",
        OutletParentsRetrieveAPIView.as_view(),
        name="outlets-parents-retrieve",
    ),
    # =====================================================
    # Staff
    # =====================================================
    path(
        "staff/<str:pk>/",
        StaffRetrieveUpdateAPIView.as_view(),
        name="staff-retrieve-update",
    ),
    path(
        "staff/<str:pk>/make-head-coordinator/",
        StaffClassesHeadCoordinatorCreateAPIView.as_view(),
        name="staff-classes-header-coordinator-create",
    ),
    # =====================================================
    # Classes
    # =====================================================
    path(
        "classes/<str:pk>/",
        ClassesRetrieveUpdateAPIView.as_view(),
        name="classes-retrieve-update",
    ),
    # =====================================================
    # Sections
    # =====================================================
    path(
        "sections/<str:pk>/",
        SectionRetrieveUpdateAPIView.as_view(),
        name="sections-retrieve-update",
    ),
    # =====================================================
    # Students
    # =====================================================
    path(
        "students/<str:pk>/",
        StudentRetrieveUpdateAPIView.as_view(),
        name="students-retrieve-update",
    ),
    # =====================================================
    # Lookups
    # =====================================================
    path("lookup/<str:flag>/", LookupListAPIView.as_view(), name="lookup-list"),
]
