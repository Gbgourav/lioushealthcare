from django.urls import path

from blood_bank.views import BloodBankDashboardAPIView
from .views import VendorCreateAPIView, GetVendorProfile

urlpatterns = [
    path('create/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('get_complete_profile/', GetVendorProfile.as_view(), name='get_complete_profile'),
]
