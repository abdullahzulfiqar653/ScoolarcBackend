from api.views.outlets.outlet import (
    OutletListCreateView,
    OutletRetrieveUpdateDestroyView,
)
from api.views.outlets.member import MemberListCreateView
from api.views.permissions import PermissionsListAPIView
from api.views.otp import OTPView
from api.views.outlets.classes import (
    ClassesListCreateView,
    ClassesRetrieveUpdateDestroyView,
)
from api.views.classes.sections import (
    ListCreateSectionView,
    RetrieveUpdateDestroySectionView,
)
__all__ = [
    "OutletListCreateView",
    "OutletRetrieveUpdateDestroyView",
    "MemberListCreateView",
    "PermissionsListAPIView",
    "OTPView",
    "ClassesListCreateView",
    "ClassesRetrieveUpdateDestroyView",
    "ListCreateSectionView",
    "RetrieveUpdateDestroySectionView",

]
