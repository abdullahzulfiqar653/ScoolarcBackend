from api.views.outlets import (
    MerchantOutletListCreateView,
    OutletClassesListCreateAPIView,
    OutletRetrieveUpdateDestroyView,

)
from api.views.classes import ClassesRetrieveUpdateAPIView
from api.views.outlets import OutletStudentListCreateAPIView
from api.views.outlets.member import OutletMemberListCreateView
from api.views.permissions import PermissionsListAPIView
from api.views.otp import OTPView
from api.views.lookup import LookupListAPIView

from api.views.classes.sections import (
    ClassListCreateSectionView,
)
from api.views.sections.section import (
    SectionRetrieveUpdateDestroyView,
)

from api.views.student import (
    StudentRetrieveUpdateDestroyView
)
from api.views.referesh_token import RefreshTokenAPIView
from api.views.images import ImagesCreateAPIView

__all__ = [
    "OTPView",
    "LookupListAPIView",
    "RefreshTokenAPIView",
    "ImagesCreateAPIView",
    "PermissionsListAPIView",
    "ClassListCreateSectionView",
    "OutletMemberListCreateView",
    "ClassesRetrieveUpdateAPIView",
    "MerchantOutletListCreateView",
    "OutletStudentListCreateAPIView",
    "OutletClassesListCreateAPIView",
    "OutletRetrieveUpdateDestroyView",
    "SectionRetrieveUpdateDestroyView",
    "StudentRetrieveUpdateDestroyView",
]
