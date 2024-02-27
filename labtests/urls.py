from django.urls import path, include

from labtests.views import GetProductListAPIView, GetLabListAPIView, adddataapu

# Create a router and register the DoctorVendorViewSet with it

urlpatterns = [

    path('lab_dashboard/', GetProductListAPIView.as_view(), name='get_pharmacy'),
    path('lab_list/', GetLabListAPIView.as_view(), name='lab_list'),
    path('update/', adddataapu.as_view(), name='update'),

]
