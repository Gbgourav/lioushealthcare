from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, contact_no, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username'), contact_no=contact_no
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, contact_no, **kwargs):
        account = self.create_user(email, contact_no, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class UserAccount(AbstractUser):
    class ProfileType(models.TextChoices):
        Consumer = 'Consumer', _('Consumer')
        Vendor = 'Vendor', _('Vendor')

    username = models.CharField(_('username'), max_length=40, blank=True, null=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(_('email address'), max_length=60, unique=True)
    first_name = models.CharField(_('first name'), max_length=40)
    type = models.CharField(_('type'), max_length=100, choices=ProfileType.choices, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=40, blank=True, null=True)
    contact_no = PhoneNumberField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_profile_completed = models.BooleanField(default=False)
    residential_address = models.TextField(blank=True, null=True)
    office_address = models.TextField(blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    is_doctor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_pathology = models.BooleanField(default=False)
    is_blood_bank = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_no']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserLocation(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Location ({self.latitude}, {self.longitude}) for {self.user.username}"
