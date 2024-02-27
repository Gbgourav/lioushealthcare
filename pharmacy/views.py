import random
from random import sample
from django.db.models import Sum, F
from django.http import JsonResponse
from rest_framework.views import APIView
from pharmacy.serializers import *
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vendor.models import BookDoctorSlot, Service, Specialization
from .models import ProductCategory, ProductSubCategory, HealthConcerns, ProductBrand, Products, ProductReview
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from uuid import uuid1


class GetPharmacyDataAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(request.user)
        categories = ProductCategory.objects.all()
        health_concerns = HealthConcerns.objects.all()
        products_queryset = Products.objects.all()
        products = random.sample(list(products_queryset), min(10, products_queryset.count()))
        value_data = list(products_queryset.values_list('uid', flat=True))
        serializer = ProductCategorySerializer(categories, many=True).data
        products_data = ProductSerializer(products, many=True, context={'user': request.user}).data

        total_price = Cart.objects.filter(user=request.user).aggregate(
            total_price=Sum(F('quantity') * F('product__price'), output_field=models.DecimalField())
        )['total_price']
        total_price = total_price or 0
        cart_count = Cart.objects.filter(product__uid__in=value_data).count()
        cart_items = list(Cart.objects.filter(product__uid__in=value_data).values_list('product__name', flat=True))

        cart_data = {
            'price': total_price,
            'count': cart_count,
            'cart_items': cart_items
        }
        health_concerns_data = HealthConcernsSerializer(health_concerns, many=True).data
        return JsonResponse({'data': serializer, 'success': True, 'products_data': products_data,
                             "health_concerns_data": health_concerns_data, 'cart_data': cart_data})


class GetSubCategoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            uid = self.request.query_params.get('uid')
            subcategory = ProductSubCategory.objects.filter(category__uid=uid)
            sub_cat = ProductSubCategorySerializer(subcategory, many=True).data
            products_data = []
            if len(sub_cat) > 0:
                products = sample(list(Products.objects.filter(category__in=subcategory)), 10)
                products_data = ProductSerializer(products, many=True, context={'user': request.user}).data
            brand = ProductBrand.objects.all()
            brand_data = ProductBrandSerializer(brand, many=True).data

            return JsonResponse(
                {'products_data': products_data, 'brand_data': brand_data, 'sub_cat': sub_cat, 'success': True})

        except Exception as e:
            print("Error", e)
            return JsonResponse({
                'success': False, 'message': 'Something went wrong!'
            })


class GetProductAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            uid = self.request.query_params.get('uid')
            product = Products.objects.filter(uid=uid).first()
            products_data = ProductSerializer(product, context={'user': request.user}).data
            review = ProductReview.objects.filter(product__uid=uid).all()
            review_data = ProductReviewSerializer(review, many=True).data
            return JsonResponse({'success': True, 'products_data': products_data, 'review_data': review_data})

        except Exception as e:
            print("Error", e)
            return JsonResponse({'success': False, 'message': 'Something went wrong'})


class GetProductListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            uid = self.request.query_params.get('uid')
            type = self.request.query_params.get('type')
            if type == 'sub_cat':
                product = Products.objects.filter(category__uid=uid)
            elif type == 'brand':
                product = Products.objects.filter(brand__uid=uid)
            elif type == 'health_concerns':
                product = Products.objects.filter(health_concerns__uid=uid)
            elif type == 'main_cat':
                category = ProductSubCategory.objects.filter(category__uid=uid).all()
                product = Products.objects.filter(category__in=category)
            else:
                product = Products.objects.filter()

            products_data = ProductSerializer(product, many=True, context={'user': request.user}).data
            return JsonResponse({'success': True, 'products_data': products_data})
        except Exception as e:
            print("Error", str(e))
            return JsonResponse({'success': False, 'message': str(e)})


class AddToCartAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            uid = request.data.get('uid')
            type = request.data.get('type')
            product = Products.objects.filter(uid=uid).first()
            cart = Cart.objects.filter(product__uid=uid, user=request.user).first()

            if cart:
                if type == 'add_more':
                    cart.quantity += 1
                    cart.save()
                elif type == 'remove':
                    if cart.quantity == 1:
                        cart.delete()
                    else:
                        cart.quantity -= 1
                        cart.save()
            else:
                cart = Cart.objects.create(product=product, user=request.user, quantity=1)

            total_price = Cart.objects.filter(user=request.user).aggregate(
                total_price=Sum(F('quantity') * F('product__price'), output_field=models.DecimalField())
            )['total_price']

            total_price = total_price or 0
            cart_count = Cart.objects.filter(user=request.user).count()
            cart_items = list(Cart.objects.filter(user=request.user).values_list('product__name', flat=True))

            cart_data = {
                'price': total_price,
                'count': cart_count,
                'cart_items': cart_items
            }

            product_data = ProductSerializer(product, context={'user': request.user}).data

            return JsonResponse(
                {'success': True, 'cart_data': cart_data, 'message': 'Item added to cart', 'product_uid': uid,
                 'product_data': product_data})

        except Exception as e:
            print("Error", str(e))
            return JsonResponse({'success': False, 'message': str(e)})


class ConfirmPaymentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            type = request.data.get('type')
            uid = request.data.get('uid')
            if type and uid:
                cart = Cart.objects.filter(product__uid=uid, user=user).first()

                if cart:
                    if type == 'add_more':
                        cart.quantity += 1
                        cart.save()
                    elif type == 'remove':
                        if cart.quantity == 1:
                            cart.delete()
                        else:
                            cart.quantity -= 1
                            cart.save()

            cart_obj = Cart.objects.filter(user=user)
            cart_data = CartDetailsSerializer(cart_obj, many=True).data
            total_price = Cart.objects.filter(user=request.user).aggregate(
                total_price=Sum(F('quantity') * F('product__price'), output_field=models.DecimalField())
            )['total_price']

            total_price = total_price or 0
            cart_count = Cart.objects.filter(user=request.user).count()
            cart_items = list(Cart.objects.filter(user=request.user).values_list('product__name', flat=True))
            cart_items_uid = list(Cart.objects.filter(user=request.user).values_list('product__uid', flat=True))

            cart_data_updated = {
                'price': total_price,
                'count': cart_count,
                'cart_items': cart_items,
                'cart_items_uid': cart_items_uid
            }

            return JsonResponse({'success': True, 'cart_data': cart_data, 'cart_data_updated': cart_data_updated})

        except Exception as e:
            print("Error", str(e))
            return JsonResponse({'success': False, 'message': str(e)})


class CreateOrder(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            payment_date = request.data.get('payment_date')
            payment_method = request.data.get('payment_method')
            product = request.data.get('product')
            amount = request.data.get('amount')
            payment_obj = Payment.objects.create(user=user, amount=amount, payment_date=payment_date,
                                                 payment_method=payment_method)
            product_list = Products.objects.filter(uid__in=product)

            order_obj = Order.objects.create(user=user, payment=payment_obj)
            order_obj.product.add(*product_list)
            order_obj.save()

            delete_cart = Cart.objects.filter(user=user).delete()

            return JsonResponse({'success': True, "order_id": order_obj.uid})

        except Exception as e:
            print("Error", str(e))
            return JsonResponse({'success': False, 'message': str(e)})


class CartDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            Cart.objects.filter(user=user).delete()
            return JsonResponse({'success': True, "message": "Cart items deleted successfully"})

        except Exception as e:
            return JsonResponse({'success': False, "error": str(e)})


@api_view(['POST'])
@transaction.atomic
def add_unique_uids(request):
    try:
        with transaction.atomic():
            models_to_update = [
                # ProductCategory,
                # ProductSubCategory,
                # HealthConcerns,
                Service,
                Specialization
                # Products
            ]

            for model in models_to_update:
                objects_without_uid = model.objects.filter()
                for obj in objects_without_uid:
                    obj.uid = uuid1()
                    obj.save()

            return Response({"message": "UUIDs added successfully."})

    except IntegrityError:
        return Response({"error": "Failed to add UUIDs. IntegrityError occurred."}, status=500)
