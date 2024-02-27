from django.conf.urls import include
from django.urls import path
from .views import PhoneNumberApiView, PhoneNumberVerificationApiView, CustomRegisterView, UserCredAPIView, \
    CoordinatesToStatePincode, GetListStatesAPIView
from dj_rest_auth.views import LoginView, LogoutView

urlpatterns = [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('auth/send/otp/', PhoneNumberApiView.as_view()),
    path('auth/user_cred/', UserCredAPIView.as_view(), name='user_credentials'),
    path('otp/verified/', PhoneNumberVerificationApiView.as_view()),
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', LogoutView.as_view(), name='token_refresh'),
    path('auth/state-pincode/', CoordinatesToStatePincode.as_view(), name='state_pincode_api'),
    path('auth/get-states/', GetListStatesAPIView.as_view(), name='state_pincode_api'),

]
