from decimal import Decimal

from django.db.models import Sum
from rest_framework import serializers
from .models import *


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubCategory
        fields = '__all__'


class HealthConcernsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthConcerns
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    offer_per = serializers.SerializerMethodField()
    real_price = serializers.SerializerMethodField()
    cart_count = serializers.SerializerMethodField()

    def get_offer_per(self, obj):
        return str('30%')

    def get_cart_count(self, obj):
        user = self.context['user']
        product_in_cart = Cart.objects.filter(user=user, product__uid=obj.uid).first()
        if product_in_cart:
            count = product_in_cart.quantity
        else:
            count = 0
        return count

    def get_real_price(self, obj):
        try:
            real_price = obj.price * Decimal('0.3') + obj.price
            return real_price
        except Exception as e:
            print("Error", e)
            return ''

    def get_brand_name(self, obj):
        try:
            return str(obj.brand.name)
        except:
            return ''

    class Meta:
        model = Products
        fields = ['added_date', 'brand_name', 'name', 'category', 'health_concerns', 'image', 'last_updated', 'uid',
                  'short_description', 'vendor', 'description', 'real_price', 'offer_per', 'price', 'id', 'cart_count']


class CartDetailsSerializer(serializers.ModelSerializer):
    offer_per = serializers.SerializerMethodField()
    price_offer = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_offer_per(self, obj):
        return str('30%')

    def get_total_price(self, obj):
        product = Products.objects.filter(uid=obj.product.uid).first()
        price = 0
        if product:
            price = product.price * obj.quantity
        return round(price, 2)

    def get_price_offer(self, obj):
        product = Products.objects.filter(uid=obj.product.uid).first()
        price = 0
        if product:
            off = product.price * Decimal(0.3) + product.price
            price = off * obj.quantity
        return round(price, 2)

    def get_product(self, obj):
        product_serializer = ProductsSerializer(obj.product)
        return product_serializer.data

    class Meta:
        model = Cart
        fields = ['product', 'uid', 'quantity', 'offer_per', 'price_offer', 'total_price']


class ProductReviewSerializer(serializers.ModelSerializer):
    review_by = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    def get_review_by(self, obj):
        try:
            return str(obj.user.first_name + " " + obj.user.last_name)
        except:
            return ''

    def get_vendor_name(self, obj):
        try:
            return str(obj.product.name)
        except:
            return ''

    def get_created_date(self, obj):
        return obj.created.strftime("%d-%m-%Y")

    class Meta:
        model = ProductReview
        fields = ['review_by', 'vendor_name', 'review', 'created_date']
