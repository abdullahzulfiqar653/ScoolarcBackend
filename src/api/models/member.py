from django.db import models
from api.models.abstract.base import BaseModel
from django.core.exceptions import ValidationError
from api.common.contants import (
    STAFF,
    PARENT,
    STUDENT,
    TEACHER,
    MERCHANT,
    PRINCIPLE,
    REGISTRAR,
)


class Member(BaseModel):
    class RoleChoices(models.TextChoices):
        STAFF = STAFF
        PARENT = PARENT
        TEACHER = TEACHER
        STUDENT = STUDENT
        MERCHANT = MERCHANT
        PRINCIPAL = PRINCIPLE
        REGISTRAR = REGISTRAR

    user = models.OneToOneField(
        "auth.User", on_delete=models.SET_NULL, related_name="profile", null=True
    )
    merchant = models.ForeignKey(
        "api.Merchant", on_delete=models.CASCADE, related_name="members"
    )
    outlets = models.ManyToManyField("api.Outlet", related_name="outlet_members")
    role = models.CharField(
        max_length=20,
        choices=[(role.value, role.name) for role in RoleChoices],
        default=RoleChoices.STUDENT,
    )
    address = models.TextField(null=True)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True)
    first_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=True)
    cnic = models.CharField(max_length=13, null=True)
    email = models.EmailField(max_length=50, null=True)
    religion = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    blood_group = models.CharField(max_length=3, null=True)
    emergency_contact = models.CharField(max_length=10, null=True)
    avatar = models.CharField(max_length=256, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(
        max_length=10
    )  # Gender reference from Lookup [Male, Female, Other]
    primary_phone = models.CharField(
        max_length=10, null=True, verbose_name="Primary Phone"
    )
    registration_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f" - {self.role} of {self.merchant.name}."

    class Meta:
        verbose_name = "MembersRegister"
        unique_together = [["user", "merchant", "role", "cnic"]]

    def clean(self):
        # Enforce that a student can only have one outlet
        if self.pk and self.role.lower() == "student":
            if self.outlets.exists() and self.outlets.count() > 1:
                raise ValidationError("A student can only be linked to one outlet.")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure validation runs before saving
        self.clean()
        super().save(*args, **kwargs)
