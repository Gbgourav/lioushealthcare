import uuid

from django.db import models

from accounts.models import UserAccount
from payment.models import Payment
from vendor.models import PathologyVendor


class HealthConcern(models.Model):
    name = models.CharField(max_length=255)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='concern/', null=True, blank=True)

    def __str__(self):
        return self.name


class HealthConcernSubCategory(models.Model):
    health_concern = models.ForeignKey(HealthConcern, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.health_concern.name} - {self.name}"


class LabTest(models.Model):
    vendor = models.ForeignKey(PathologyVendor, on_delete=models.CASCADE, related_name="labtests")
    sub_category = models.ForeignKey(HealthConcernSubCategory, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    related_tests = models.ManyToManyField('self', symmetrical=False, blank=True)
    total_tests_count = models.IntegerField(default=1, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vendor} - {self.sub_category.name} - {self.name}"


class LabCart(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_lab_cart')
    product = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='user_test')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class TestOrder(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='test_user')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payments_for_test', null=True,
                                blank=True)
    test = models.ForeignKey(LabCart, on_delete=models.CASCADE, related_name='test_product', null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_delivered = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    delivered_data = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
