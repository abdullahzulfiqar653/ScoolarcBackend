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
from api.views.parents import (
    ParentsOTPView,
    ParentsRetrieveUpdateAPIView,
)

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
    StaffPermissionsListAPIView,
    StaffClassesHeadCoordinatorListCreateAPIView,
)


from api.views.permissions import PermissionsListAPIView
from api.views.section import SectionRetrieveUpdateAPIView
from api.views.student import StudentRetrieveUpdateAPIView

__all__ = [
    OTPView,
    ParentsOTPView,
    LookupListAPIView,
    RefreshTokenAPIView,
    ImagesCreateAPIView,
    SubjectUpdateAPIView,
    PermissionsListAPIView,
    OutletParentsListAPIView,
    ClassSectionCreateAPIView,
    StaffRetrieveUpdateAPIView,
    StaffPermissionsListAPIView,
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
