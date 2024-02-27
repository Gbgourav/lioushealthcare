from django.urls import path, include

from pharmacy.views import GetPharmacyDataAPIView, add_unique_uids, GetSubCategoryAPIView, GetProductAPIView, \
    GetProductListAPIView, AddToCartAPIView, ConfirmPaymentAPIView, CreateOrder, CartDeleteAPIView

# Create a router and register the DoctorVendorViewSet with it

urlpatterns = [

    path('get_pharmacy/', GetPharmacyDataAPIView.as_view(), name='get_pharmacy'),
    path('add-unique-uids/', add_unique_uids, name='add_unique_uids'),
    path('get_sub_cat/', GetSubCategoryAPIView.as_view(), name='get_sub_cat'),
    path('add_to_cart/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('confirm_pay/', ConfirmPaymentAPIView.as_view(), name='add_to_cart'),
    path('get_product/', GetProductAPIView.as_view(), name='get_product'),
    path('get_product_list/', GetProductListAPIView.as_view(), name='get_product_list'),
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('delete_cart/', CartDeleteAPIView.as_view(), name='delete_cart'),

]
