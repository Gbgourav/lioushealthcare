import uuid

from django.db import models

from vendor.models import PharmacyVendor, BloodBankVendor


# Create your models here.


class BloodGroup(models.Model):
    name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class BloodType(models.Model):
    name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class BloodBank(models.Model):
    vendor = models.ForeignKey(BloodBankVendor, on_delete=models.CASCADE, related_name="bloodBank")
    name = models.TextField(max_length=100)
    address = models.TextField(max_length=100, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    contact_number = models.CharField(max_length=20, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blood_bank/', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class BloodBankStock(models.Model):
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name="bloodBankStock")
    type = models.ForeignKey(BloodType, on_delete=models.CASCADE, related_name="BloodType")
    group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE, related_name="BloodGroup", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    uid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)

    def __str__(self):
        return str(self.bank)


class BloodStock(models.Model):
    bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name="blood_bank_stock")
    type = models.ForeignKey(BloodType, on_delete=models.CASCADE, related_name="blood_type")
    a_positive = models.BooleanField(default=False)
    b_positive = models.BooleanField(default=False)
    o_positive = models.BooleanField(default=False)
    ab_positive = models.BooleanField(default=False)
    a_negative = models.BooleanField(default=False)
    b_negative = models.BooleanField(default=False)
    o_negative = models.BooleanField(default=False)
    ab_negative = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    uid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)

    def __str__(self):
        return str(self.bank)
