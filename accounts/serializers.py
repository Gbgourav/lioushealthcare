from phonenumber_field.validators import validate_international_phonenumber
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from phone_numbers.models import PhoneNumber
from rest_framework.authtoken.models import Token

import string
import secrets

UserAccount = get_user_model()


def generate_random_password(length=8):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    if not any(c.isupper() for c in password):
        # if no uppercase letters, replace a random character with an uppercase letter
        password = list(password)
        idx = secrets.randbelow(length)
        password[idx] = secrets.choice(string.ascii_uppercase)
        password = ''.join(password)
    return password


class UserAccountListSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'contact_no')


class CustomRegisterSerializer(RegisterSerializer):
    password1 = None
    password2 = None
    username = None
    access_token = serializers.SerializerMethodField()
    first_name = serializers.CharField(required=True, min_length=3)
    last_name = serializers.CharField(required=False, min_length=3)
    uid = serializers.UUIDField()

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'uid': self.validated_data.get('uid', ''),
        }

    def validate(self, attrs):
        attrs['password1'] = generate_random_password(8)
        attrs['password2'] = attrs['password1']
        return super().validate(attrs)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        phone_numbers_obj = PhoneNumber.objects.get(uid=self.cleaned_data.get('uid'))
        user.contact_no = phone_numbers_obj.contact_no
        user.save()
        return user

    def get_access_token(self, obj):
        try:
            token = Token.objects.get(user__email=self.validated_data.get('email', ''))
        except Exception as e:
            obj = UserAccount.objects.get(email=self.validated_data.get('email', ''))
            token = Token.objects.create(user=obj)
        return token.key

    def create(self, validated_data):
        user = super().create(validated_data)
        access_token = self.get_access_token(user)
        data = {'user': user, 'access_token': access_token}
        return Response(data, status=status.HTTP_201_CREATED)


class SendOtpLoginSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15, validators=[validate_international_phonenumber])

    class Meta:
        fields = ['contact_no']


class GetPhoneNumberSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15, validators=[validate_international_phonenumber])

    class Meta:
        fields = ['number']


class PhoneNumberOtpSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=15, validators=[validate_international_phonenumber])
    otp_value = serializers.CharField(max_length=6)

    class Meta:
        fields = ['otp_value', 'number']


class CountrysideSerializer(serializers.Serializer):
    class Meta:
        model = UserAccount
        list_display = ['country']
