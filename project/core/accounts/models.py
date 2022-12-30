from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="address"
    )
    editable = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mobile = models.CharField(max_length=20)
    landline = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.CharField(max_length=2000)
    address2 = models.CharField(max_length=2000, null=True, blank=True)
    landmark = models.CharField(max_length=1000)
    pincode = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.pincode}"

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name_plural = "Address Entries"
