from api.serializers.classes import ClassesSerializer
from api.serializers.section_resource_assignment import (
    ClassSectionResourceAssignmentSerializer,
    ClassSectionResourceAssignmentRetrieveSerializer,
)
from api.permissions import RolePermission, IsOutletMember

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView


@extend_schema(
    methods=["GET"],
    description="Retrieve class details by ID, including its associated sections.",
    responses={200: ClassesSerializer},
)
@extend_schema(
    methods=["PUT", "PATCH"],
    description=(
        "Update class name only." "`class_sections` not required in update requests."
    ),
    request=ClassesSerializer,
    responses={200: ClassesSerializer},
)
class ClassesRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ClassesSerializer
    permission_classes = [IsOutletMember, RolePermission]

    def get_queryset(self):
        return self.request.classes.outlet.outlet_classes.all()


@extend_schema(
    methods=["GET"],
    description=(
        "Retrieve the assigned teacher-subject pairs and coordinator of a section.\n\n"
        "**Notes:**\n"
        "- `section_teacher_and_subject`: A list of objects each containing a `teacher` (Staff ID) and a `book` (Subject ID).\n"
        "- `coordinator`: Staff ID who is set as the class coordinator."
    ),
    responses={200: ClassSectionResourceAssignmentRetrieveSerializer},
)
@extend_schema(
    methods=["PUT", "PATCH"],
    description=(
        "Assign teacher-subject pairs to a section, and set a class coordinator.\n\n"
        "**Notes:**\n"
        "- `section_teacher_and_subject` must be a list of objects, each with a `teacher` (Staff ID) and a `book` (Subject ID).\n"
        "- `coordinator` must be a valid Staff ID from the `teacher` list.\n"
        "- Any previous teacher-subject assignments for this section will be removed and replaced."
    ),
    request=ClassSectionResourceAssignmentSerializer,
    responses={200: ClassSectionResourceAssignmentSerializer},
)
class ClassSectionResourceAssignmentRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsOutletMember, RolePermission]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClassSectionResourceAssignmentRetrieveSerializer
        return ClassSectionResourceAssignmentSerializer

    def get_object(self):
        section_id = self.kwargs.get("section_id")
        return get_object_or_404(self.request.classes.class_sections, id=section_id)

    def get_queryset(self):
        return self.request.classes.outlet.outlet_classes.all()
