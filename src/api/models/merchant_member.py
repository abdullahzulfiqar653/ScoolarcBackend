from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from api.models.lookup import Lookup
from api.models.outlet import Outlet
from api.models.merchant import Merchant
from api.models.abstract.base import BaseModel


class MerchantMember(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member_profile"
    )
    merchant = models.ForeignKey(
        Merchant, on_delete=models.CASCADE, related_name="merchant_member"
    )
    outlets = models.ManyToManyField(Outlet)
    role = models.ForeignKey(
        Lookup, on_delete=models.CASCADE
    )  # Dynamic role reference[merchant, principal, admin, teacher, student]
    address = models.TextField(null=True)
    status = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    cnic = models.CharField(max_length=13, null=True)
    avatar = models.ImageField(upload_to="protected/avatars", null=True)
    emergency_contact = models.CharField(max_length=10, null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    blood_group = models.CharField(max_length=3, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.ForeignKey(
        Lookup, on_delete=models.CASCADE, related_name="gender"
    )  # Gender reference from Lookup [Male, Female, Other]
    phone = models.CharField(max_length=10, null=True, verbose_name="Primary Phone")
    phone_network = models.ForeignKey(
        Lookup, on_delete=models.CASCADE, related_name="network", null=True
    )  # Network reference from Lookup
    registration_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.name} of {self.merchant.name}."

    class Meta:
        verbose_name = "MerchantsMembersRegister"
        unique_together = [["user", "merchant", "role", "cnic", "status"]]

    def clean(self):
        # Enforce that a student can only have one outlet
        if self.role.name.lower() == "student" and self.outlets.count() >= 1:
            raise ValidationError("A student can only be linked to one outlet.")
            # Enforce phone uniqueness logic
        # if self.phone:
        #     # Fetch other members with the same phone number
        #     existing_member = (
        #         MerchantMember.objects.filter(phone=self.phone)
        #         .exclude(pk=self.pk)
        #         .first()
        #     )

        #     if existing_member:
        #         # If the existing member is a parent, check if this user is their child
        #         if existing_member.role.name.lower() == "parent":
        #             # Check if this user is a student linked to the parent
        #             parent_relation = StudentParent.objects.filter(
        #                 parent=existing_member, student=self
        #             ).exists()
        #             if not parent_relation:
        #                 raise ValidationError(
        #                     "This phone number is already assigned to another parent."
        #                 )
        #         else:
        #             raise ValidationError(
        #                 "This phone number is already assigned to another user."
        #             )

        super().clean()

    def save(self, *args, **kwargs):
        # Ensure validation runs before saving
        self.clean()
        super().save(*args, **kwargs)
