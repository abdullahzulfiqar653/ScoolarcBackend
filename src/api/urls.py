from django.urls import path, include
from api.views import (
    OTPView,
    LookupListAPIView,
    ImagesCreateAPIView,
    RefreshTokenAPIView,
    SubjectUpdateAPIView,
    PermissionsListAPIView,
    OutletParentsListAPIView,
    ClassSectionCreateAPIView,
    StaffRetrieveUpdateAPIView,
    StaffPermissionsListAPIView,
    OutletParentsRetrieveAPIView,
    MerchantOutletListCreateView,
    ClassesRetrieveUpdateAPIView,
    SectionRetrieveUpdateAPIView,
    StudentRetrieveUpdateAPIView,
    OutletStaffListCreateAPIView,
    ParentsRetrieveUpdateAPIView,
    ClassSectionBulkCreateAPIView,
    ClassSubjectListCreateAPIView,
    ClassSubjectBulkCreateAPIView,
    OutletStudentListCreateAPIView,
    OutletClassesListCreateAPIView,
    OutletRetrieveUpdateDestroyView,
    ClassSectionResourceAssignmentRetrieveUpdateAPIView,
    StaffClassesHeadCoordinatorListCreateAPIView,
)

urlpatterns = [
    # =====================================================
    # Auth
    # =====================================================
    path("auth/", include("rest_framework.urls")),
    path("auth/token/", OTPView.as_view(), name="token_obtain_pair"),
    path("auth/image-upload/", ImagesCreateAPIView.as_view(), name="presigned-url"),
    path("auth/token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
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
        "staff/<str:pk>/permissions/",
        StaffPermissionsListAPIView.as_view(),
        name="staff-permissions-list-view",
    ),
    path(
        "staff/<str:staff_id>/classes-head-coordinator/",
        StaffClassesHeadCoordinatorListCreateAPIView.as_view(),
        name="staff-classes-head-coordinator-list-create",
    ),
    # =====================================================
    # Classes
    # =====================================================
    path(
        "classes/<str:pk>/",
        ClassesRetrieveUpdateAPIView.as_view(),
        name="classes-retrieve-update",
    ),
    path(
        "classes/<str:pk>/subjects",
        ClassSubjectListCreateAPIView.as_view(),
        name="subject-list-create-view",
    ),
    path(
        "classes/<str:pk>/subjects/bulk-create",
        ClassSubjectBulkCreateAPIView.as_view(),
        name="subject-bulk-create-view",
    ),
    path(
        "classes/<str:pk>/sections",
        ClassSectionCreateAPIView.as_view(),
        name="classes-create-view",
    ),
    path(
        "classes/<str:pk>/sections/bulk-create",
        ClassSectionBulkCreateAPIView.as_view(),
        name="subject-bulk-create-view",
    ),
    path(
        "classes/<str:pk>/sections/<str:section_id>/",
        ClassSectionResourceAssignmentRetrieveUpdateAPIView.as_view(),
        name="class-section-resource-assignment-view",
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
        name="students-retrieve-update-view",
    ),
    # =====================================================
    # Parents
    # =====================================================
    path(
        "parents/<str:pk>/",
        ParentsRetrieveUpdateAPIView.as_view(),
        name="parents-retrieve-update-view",
    ),
    # =====================================================
    # Subjects
    # =====================================================
    path(
        "subjects/<str:pk>/",
        SubjectUpdateAPIView.as_view(),
        name="subject-update-view",
    ),
    # =====================================================
    # Lookups
    # =====================================================
    path("lookup/<str:flag>/", LookupListAPIView.as_view(), name="lookup-list"),
]
