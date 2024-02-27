from rest_framework import serializers

from accounts.models import State
from accounts.serializers import UserAccountListSerializers
from .models import DoctorVendor, PathologyVendor, PhlebologistVendor, PharmacyVendor, Slot, SlotTime, BookDoctorSlot, \
    Review, Timing, Service, Specialization, Facilities, BloodBankVendor
from datetime import datetime, timedelta


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_name']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['specialization_name']


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = ['facility_name']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['name']


class DoctorVendorSerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = DoctorVendor
        fields = '__all__'


class BloodBankVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBankVendor
        fields = '__all__'


class PathologyVendorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PathologyVendor
        fields = '__all__'


class PhlebologistVendorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PhlebologistVendor
        fields = '__all__'


class PharmacyVendorSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PharmacyVendor
        fields = '__all__'


class SlotTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotTime
        fields = ['start_time', "end_time"]


class ReviewSerializer(serializers.ModelSerializer):
    review_by = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    def get_review_by(self, obj):
        try:
            return str(obj.user.first_name + " " + obj.user.last_name)
        except:
            return ''

    def get_vendor_name(self, obj):
        try:
            return str(obj.vendor.first_name + " " + obj.vendor.last_name)
        except:
            return ''

    def get_created_date(self, obj):
        return obj.created.strftime("%d-%m-%Y")

    class Meta:
        model = Review
        fields = ['review_by', 'vendor_name', 'review', 'created_date']


class TimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timing
        fields = ['day', 'start_time', 'end_time']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['service_name', 'uid']


class SpecializationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['specialization_name', 'uid']


class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = '__all__'


class BookDoctorSlotSerializer(serializers.ModelSerializer):
    customer = UserAccountListSerializers()

    class Meta:
        model = BookDoctorSlot
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    morning_times = serializers.SerializerMethodField()
    afternoon_times = serializers.SerializerMethodField()
    evening_times = serializers.SerializerMethodField()
    night_times = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ['day', 'id', 'morning_times', 'afternoon_times', 'evening_times', 'night_times']

    def get_morning_times(self, obj):
        return self.get_slot_times(obj, 10, 12)

    def get_afternoon_times(self, obj):
        return self.get_slot_times(obj, 12, 16)

    def get_evening_times(self, obj):
        return self.get_slot_times(obj, 16, 20)

    def get_night_times(self, obj):
        return self.get_slot_times(obj, 21, 22)

    def get_slot_times(self, obj, start_hour, end_hour=None):
        slot_available = self.context.get('slot_available', [])
        day_of_week_string = self.context.get('day_of_week_string', '')
        slots = []
        for st in obj.slot_times.all():
            if obj.day == day_of_week_string:
                slots.append({'start_time': st.start_time, 'end_time': st.end_time,
                              'active': st.start_time not in slot_available})
            else:
                slots.append({'start_time': st.start_time, 'end_time': st.end_time, 'active': True})

        slots = [
            {'start_time': st['start_time'], 'active': st['active'], 'end_time': st['end_time']}
            for st in slots
            if start_hour <= st['start_time'].hour < (end_hour if end_hour else 24)
        ]
        return slots
