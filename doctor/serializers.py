# doctor/serializers.py
from rest_framework import serializers

from vendor.models import Specialization, BookDoctorSlot
from .models import DoctorType


class DoctorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class BookDoctorSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDoctorSlot
        fields = '__all__'
