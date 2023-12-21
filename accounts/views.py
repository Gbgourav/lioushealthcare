from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from rest_framework.generics import  GenericAPIView
from rest_framework import status
from django.conf import settings
from phone_numbers.models import PhoneNumber
from .serializers import GetPhoneNumberSerializer, PhoneNumberOtpSerializer, CountrysideSerializer
from .models import UserAccount
from twilio.rest import verify, Client
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
import re
import uuid
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler
import time
import datetime


def generate_jwt_tokens(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    payload['token_type'] = 'access'
    payload['exp'] = int(time.mktime((datetime.datetime.utcnow() + datetime.timedelta(days=5)).timetuple()))
    payload['iat'] = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    payload['jti'] = '7b3bc34f68024c628a6ea783036c6f6c'

    access_token = jwt_encode_handler(payload)

    return access_token, access_token
#
#
# def send_push_notification(**kwargs):
#     gcm_reg_id = kwargs.get("gcm_reg_id")
#     device = GCMDevice.objects.get(registration_id=gcm_reg_id)
#     device.send_message("test message")
#
#     device.send_message(None, extra={"foo": "bar"})


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)


def send(phone):
    try:
        verify.verifications.create(to=phone, channel='sms')
    except Exception as e:
        print(str(e))
        print(str(e))


def check(number, otp):
    try:
        result = verify.verification_checks.create(to=number, code=otp)
    except TwilioRestException:
        return False
    return result.status == 'approved'


class PhoneNumberApiView(APIView):
    serializer_class = GetPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['number']
            raw_number = re.sub('\W+', '', phone)
            if settings.DEBUG:
                send(phone)
            return Response({"message": str('OTP successfully sent to your Number')}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhoneNumberVerificationApiView(GenericAPIView):
    serializer_class = PhoneNumberOtpSerializer

    def post(self, request):
        otp = request.data.get('otp_value')
        number = request.data.get('number')
        if settings.DEBUG:
            if check(number, otp):
                if UserAccount.objects.filter(contact_no=number).exists():
                    obj = UserAccount.objects.filter(contact_no=number).first()
                    # token = Token.objects.filter(user__email=obj.email).first()
                    # token, created = Token.objects.get_or_create(user=request.user)
                    access_token, refresh_token = generate_jwt_tokens(obj)
                    return Response({'message': str('You Have Been verified'), "access_token": access_token,
                                     "refresh_token": refresh_token},
                                    status=status.HTTP_200_OK)
                else:
                    try:
                        uid_value = uuid.uuid4()
                        PhoneNumber.objects.create(uid=uid_value, contact_no=number)
                        return Response({'message': str(uid_value)}, status=status.HTTP_200_OK)
                    except:
                        return Response({"error": str('OTP Not Verified')}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": str('OTP Not Verified')}, status=status.HTTP_400_BAD_REQUEST)
        elif otp == '111111':
            return Response({'message': str('You Have Been verified')}, status=status.HTTP_200_OK)
        else:
            return Response({"error": str('OTP Not Verified')}, status=status.HTTP_400_BAD_REQUEST)


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer







