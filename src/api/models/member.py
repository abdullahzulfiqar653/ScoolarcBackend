from django.db import models
from api.models.abstract.base import BaseModel
from django.core.exceptions import ValidationError


class Member(BaseModel):
    user = models.OneToOneField(
        "auth.User", on_delete=models.SET_NULL, related_name="profile", null=True
    )
    merchant = models.ForeignKey(
        "api.Merchant", on_delete=models.CASCADE, related_name="members"
    )
    outlets = models.ManyToManyField("api.Outlet", related_name="outlet_members")
    role = models.CharField(
        max_length=20
    )  # [merchant, principal, admin, teacher, student]
    address = models.TextField(null=True)
    status = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    cnic = models.CharField(max_length=13, null=True)
    avatar = models.ImageField(upload_to="protected/avatars", null=True)
    emergency_contact = models.CharField(max_length=10, null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    blood_group = models.CharField(max_length=3, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(
        max_length=10
    )  # Gender reference from Lookup [Male, Female, Other]
    phone = models.CharField(max_length=10, null=True, verbose_name="Primary Phone")
    phone_network = models.CharField(
        max_length=10
    )  # [ Jazz, Ufone, Zong, Telenor, Warid]
    registration_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name} of {self.merchant.name}."

    class Meta:
        verbose_name = "MembersRegister"
        unique_together = [["user", "merchant", "role", "cnic"]]

    def clean(self):
        # Enforce that a student can only have one outlet
        if self.role.name.lower() == "student" and self.outlets.count() > 1:
            raise ValidationError("A student can only be linked to one outlet.")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure validation runs before saving
        self.clean()
        super().save(*args, **kwargs)
