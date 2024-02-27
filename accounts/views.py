from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from rest_framework.generics import GenericAPIView
from django.conf import settings
from phone_numbers.models import PhoneNumber
from vendor.models import Vendor
from .serializers import GetPhoneNumberSerializer, PhoneNumberOtpSerializer, CountrysideSerializer, \
    UserAccountListSerializers, CoordinatesSerializer, StateSerializer
from .models import UserAccount, State
from twilio.rest import verify, Client
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
import re
import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_encode_handler
import time
import datetime
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import random
import string
import requests
from geopy.geocoders import Nominatim


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
        return True
    except Exception as e:
        print(str(e))
        return False


def check(number, otp):
    try:
        result = verify.verification_checks.create(to=number, code=otp)
    except TwilioRestException:
        return False
    return result.status == 'approved'


class PhoneNumberApiView(APIView):
    serializer_class = GetPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                phone = serializer.validated_data['number']
                raw_number = re.sub('\W+', '', phone)
                if settings.DEBUG:
                    if send(phone):
                        return JsonResponse({"message": 'OTP successfully sent to your Number', "success": True})
                    else:
                        return JsonResponse({"message": "Could not send the sms please try again.", "success": False})

            return JsonResponse({"message": serializer.errors, "success": False})

        except Exception as e:
            return JsonResponse({"message": str(e), "success": False})


class PhoneNumberVerificationApiView(GenericAPIView):
    serializer_class = PhoneNumberOtpSerializer

    def post(self, request):
        otp = request.data.get('otp_value')
        number = request.data.get('number')
        if settings.DEBUG:
            if check(number, otp):
                if UserAccount.objects.filter(contact_no=number).exists():
                    user_obj = UserAccount.objects.filter(contact_no=number).first()
                    serializer = UserAccountListSerializers(user_obj)
                    serialized_user = serializer.data
                    access_token = Token.objects.get(user=user_obj).key

                    response_data = {
                        'success': True,
                        'is_reg': True,
                        'user': {
                            **serialized_user,
                            'access_token': access_token,
                        }
                    }
                    return JsonResponse(response_data)
                else:
                    try:
                        uid_value = uuid.uuid4()
                        PhoneNumber.objects.create(uid=uid_value, contact_no=number)
                        return JsonResponse({'success': True, 'uid': uid_value, 'is_reg': False})
                    except Exception as e:
                        print("Error", e)
                        return JsonResponse({'success': False, 'message': "OTP not valid"})
            else:
                return JsonResponse({'success': False, 'message': "OTP not valid"})
        else:
            return JsonResponse({'success': False, 'message': "OTP not valid"})


def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse({"user": serializer.data, "success": True})


class UserCredAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            print(request.headers)
            user = request.user
            if user:
                user_data = UserAccount.objects.get(email=user.email)
                if user_data:
                    serializer = UserAccountListSerializers(user_data)
                    serialized_user = serializer.data
                    return JsonResponse({"success": True, "data": serialized_user})
                else:
                    return JsonResponse({'success': False, "message": "User not found"})
            else:
                return JsonResponse({"success": False, "message": "user token is required"})

        except Exception as e:
            return JsonResponse({'success': False, "message": str(e)})


class GoogleAuthAPIView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token')

        google_response = self.verify_google_token(access_token)

        if google_response.get('error'):
            return Response({'error': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = google_response.get('user_info')

        return Response({'success': True, 'user_info': user_info}, status=status.HTTP_200_OK)

    def verify_google_token(self, access_token):
        # Make a request to Google's token info endpoint
        google_response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo',
                                       params={'access_token': access_token}).json()

        return google_response


class CoordinatesToStatePincode(APIView):
    def post(self, request):
        try:
            serializer = CoordinatesSerializer(data=request.data)
            if serializer.is_valid():
                latitude = serializer.validated_data.get('latitude')
                longitude = serializer.validated_data.get('longitude')
                geolocator = Nominatim(user_agent="lioushealthcare")
                location = geolocator.reverse(f"{latitude}, {longitude}")
                address = location.raw['address']
                state = address.get('state', '')
                pincode = address.get('postcode', '')
                return Response({'state': state, 'pincode': pincode})
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'success': False, "message": str(e)})


class LocationInfoFromPincodeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pincode = request.query_params.get('pincode')

        try:
            geolocator = Nominatim(user_agent="my_application")
            location = geolocator.geocode(query=f"{pincode}, India", exactly_one=True)
            if location:
                state = location.raw.get('state', ''),
                place = location.raw.get('display_name', ''),
            else:
                return {'error': 'Location not found for the given pincode'}
        except Exception as e:
            return {'error': str(e)}


class GetListStatesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            state = State.objects.filter()
            state_data = StateSerializer(state, many=True).data
            return JsonResponse({'states': state_data, 'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
