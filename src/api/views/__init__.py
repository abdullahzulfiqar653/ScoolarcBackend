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

from api.views.otp import OTPView, AppOtpView
from api.views.lookup import LookupListAPIView
from api.views.images import ImagesCreateAPIView
from api.views.refresh_token import RefreshTokenAPIView, AppRefreshTokenAPIView

from api.views.staff import (
    StaffRetrieveUpdateAPIView,
    StaffPermissionsListAPIView,
    StaffClassesHeadCoordinatorListCreateAPIView,
)


from api.views.section import SectionRetrieveUpdateAPIView
from api.views.student import StudentRetrieveUpdateAPIView
from api.views.permissions import PermissionsListCreateAPIView

from api.views.parents_app import (
    GuardianOutletListView,
    GuardianStudentListView,
)

__all__ = [
    OTPView,
    AppOtpView,
    ParentsOTPView,
    LookupListAPIView,
    RefreshTokenAPIView,
    ImagesCreateAPIView,
    SubjectUpdateAPIView,
    GuardianOutletListView,
    AppRefreshTokenAPIView,
    GuardianStudentListView,
    OutletParentsListAPIView,
    ClassSectionCreateAPIView,
    StaffRetrieveUpdateAPIView,
    StaffPermissionsListAPIView,
    PermissionsListCreateAPIView,
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
