from api.views.outlets.outlet import (
    MerchantOutletListCreateView,
    OutletRetrieveUpdateDestroyView,
)
from api.views.outlets.member import OutletMemberListCreateView
from api.views.permissions import PermissionsListAPIView
from api.views.otp import OTPView
from api.views.outlets.classes import (
    OutletClassesListCreateView,
)
from api.views.classes.sections import (
    ClassListCreateSectionView,
)
from api.views.sections.section import (
    SectionRetrieveUpdateDestroyView,
)
from api.views.sections.student import (
    SectionListCreateStudentView
)
from api.views.student import (
    StudentRetrieveUpdateDestroyView
)
from api.views.referesh_token import RefreshTokenAPIView

__all__ = [
    "MerchantOutletListCreateView",
    "OutletRetrieveUpdateDestroyView",
    "SectionListCreateStudentView",
    "OutletMemberListCreateView",
    "PermissionsListAPIView",
    "OTPView",
    "RefreshTokenAPIView",
    "OutletClassesListCreateView",
    "ClassListCreateSectionView",
    "SectionRetrieveUpdateDestroyView",
    "StudentRetrieveUpdateDestroyView",

]
