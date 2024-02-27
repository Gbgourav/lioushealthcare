from django.urls import path, include

from blood_bank.views import add_unique_uids, BloodBankDashboardAPIView, BloodBankGroupAPIView, \
    BloodBankDataAPIView

urlpatterns = [
    path('dummy_data/', add_unique_uids, name='add_unique_uids_new'),
    path('get_blood_bank_dashboard/', BloodBankDashboardAPIView.as_view(), name='get_blood_bank_dashboard'),
    path('get_blood_bank_by_group/', BloodBankGroupAPIView.as_view(), name='get_blood_bank_by_group'),
    path('get_blood_bank/', BloodBankDataAPIView.as_view(), name='get_blood_bank'),
]
