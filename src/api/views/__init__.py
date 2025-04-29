from api.views.outlets import (
    OutletParentsListAPIView,
    MerchantOutletListCreateView,
    OutletParentsRetrieveAPIView,
    OutletStaffListCreateAPIView,
    OutletClassesListCreateAPIView,
    OutletStudentListCreateAPIView,
    OutletRetrieveUpdateDestroyView,
)

from api.views.subject import SubjectUpdateAPIView
from api.views.guardian import ParentsRetrieveUpdateAPIView

from api.views.classes import (
    ClassSectionCreateAPIView,
    ClassesRetrieveUpdateAPIView,
    ClassSubjectListCreateAPIView,
    ClassSubjectBulkCreateAPIView,
    ClassSectionBulkCreateAPIView,
    ClassSectionResourceAssignmentRetrieveUpdateAPIView,
)

from api.views.otp import OTPView
from api.views.lookup import LookupListAPIView
from api.views.images import ImagesCreateAPIView
from api.views.refresh_token import RefreshTokenAPIView

from api.views.staff import (
    StaffRetrieveUpdateAPIView,
    StaffClassesHeadCoordinatorListCreateAPIView,
)
from api.views.permissions import PermissionsListAPIView
from api.views.section import SectionRetrieveUpdateAPIView
from api.views.student import StudentRetrieveUpdateAPIView

__all__ = [
    OTPView,
    LookupListAPIView,
    RefreshTokenAPIView,
    ImagesCreateAPIView,
    SubjectUpdateAPIView,
    PermissionsListAPIView,
    OutletParentsListAPIView,
    ClassSectionCreateAPIView,
    StaffRetrieveUpdateAPIView,
    OutletStaffListCreateAPIView,
    OutletParentsRetrieveAPIView,
    ClassesRetrieveUpdateAPIView,
    SectionRetrieveUpdateAPIView,
    MerchantOutletListCreateView,
    StudentRetrieveUpdateAPIView,
    ParentsRetrieveUpdateAPIView,
    ClassSubjectListCreateAPIView,
    ClassSubjectBulkCreateAPIView,
    ClassSectionBulkCreateAPIView,
    OutletStudentListCreateAPIView,
    OutletClassesListCreateAPIView,
    OutletRetrieveUpdateDestroyView,
    StaffClassesHeadCoordinatorListCreateAPIView,
    ClassSectionResourceAssignmentRetrieveUpdateAPIView,
]
