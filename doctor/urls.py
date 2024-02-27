from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorTypeListView, DoctorVendorViewSet, SlotListAPIView, DoctorProfileAPIView, ConfirmSlot, Payment, \
    GetInitialDataView, BookDoctorSlotAPIView

# Create a router and register the DoctorVendorViewSet with it
router = DefaultRouter()

urlpatterns = [
    path('doctor-types/', DoctorTypeListView.as_view(), name='doctor_type_api'),
    path('doctor-vendors/uid=<str:uid>/', DoctorVendorViewSet.as_view(), name='doctor-vendor'),
    path('cost/', ConfirmSlot.as_view(), name='cost_api'),
    path('init/', GetInitialDataView.as_view(), name='init'),
    path('payment/', Payment.as_view(), name='payment_api'),
    path('get_slots_data/', BookDoctorSlotAPIView.as_view(), name='get_slots_data'),
    path('doctor-profile/uid=<str:uid>/', DoctorProfileAPIView.as_view(), name='doctor_profile_api'),
    path('slots/uid=<str:uid>/date=<str:date>/type=<str:type>', SlotListAPIView.as_view(), name='slot-list'),
    path('', include(router.urls)),
]
