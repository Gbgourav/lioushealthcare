import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from payment.models import Payment
from vendor.models import PharmacyVendor

UserAccount = get_user_model()


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ProductSubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='sub_category_images/', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class HealthConcerns(models.Model):
    name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='health_concerns/', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ProductBrand(models.Model):
    name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    image = models.ImageField(upload_to='brand/', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ProductRating(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    rating = models.IntegerField()
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class ProductOffer(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    vendor = models.ForeignKey(PharmacyVendor, on_delete=models.CASCADE)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    health_concerns = models.ForeignKey(HealthConcerns, on_delete=models.CASCADE, blank=True, null=True)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='product/', null=True, blank=True)

    def average_rating(self):
        ratings = ProductRating.objects.filter(product=self)
        if ratings.exists():
            return sum([rating.rating for rating in ratings]) / len(ratings)
        return 0

    def current_offer(self):
        now = timezone.now()
        try:
            return ProductOffer.objects.get(product=self, start_date__lte=now, end_date__gte=now)
        except ProductOffer.DoesNotExist:
            return None

    def __str__(self):
        return str(self.name)


class ProductReview(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_reviews_product')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_reviews')
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product.name)


class Cart(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_cart')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='user_product')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='buyer')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    product = models.ManyToManyField(Products, related_name='order_products')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_delivered = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    delivered_data = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
    
