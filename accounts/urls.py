from django.conf.urls import include
from django.urls import path
from .views import PhoneNumberApiView, PhoneNumberVerificationApiView, CustomRegisterView
from dj_rest_auth.views import LoginView, LogoutView


urlpatterns = [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='rest_register'),
    path('auth/send/otp/', PhoneNumberApiView.as_view()),
    path('otp/verified/', PhoneNumberVerificationApiView.as_view()),
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', LogoutView.as_view(), name='token_refresh'),
]