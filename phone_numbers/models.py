from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class PhoneNumber(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    contact_no = PhoneNumberField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.contact_no
