import uuid
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import State
from doctor.models import DoctorType

# from django.contrib.gis.db import models

UserAccount = get_user_model()


class DayChoices(models.TextChoices):
    MONDAY = 'Mon', 'Monday'
    TUESDAY = 'Tue', 'Tuesday'
    WEDNESDAY = 'Wed', 'Wednesday'
    THURSDAY = 'Thu', 'Thursday'
    FRIDAY = 'Fri', 'Friday'
    SATURDAY = 'Sat', 'Saturday'
    SUNDAY = 'Sun', 'Sunday'


class ServiceChoices(models.TextChoices):
    Video_Consultation = 'Video Consultation', 'Video_Consultation'
    Clinic_Visit = 'Clinic Visit', 'Clinic_Visit'


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.service_name)


class Facilities(models.Model):
    facility_name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return str(self.facility_name)


class Specialization(models.Model):
    specialization_name = models.CharField(max_length=100)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    image = models.ImageField(upload_to='specialization/', null=True, blank=True)

    def __str__(self):
        return str(self.specialization_name)


class Vendor(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='%(class)s_details')
    establishment_name = models.CharField(max_length=100)
    address = models.TextField()
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)
    contact = PhoneNumberField(max_length=20)
    is_activated = models.BooleanField(default=False)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    timing = models.CharField(max_length=100)
    services = models.ManyToManyField(Service, null=True, blank=True)
    specializations = models.ManyToManyField(Specialization, null=True, blank=True)
    facilities = models.ManyToManyField(Facilities, null=True, blank=True)

    class Meta:
        abstract = True


class Timing(models.Model):
    vendor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='vendor_timings')
    day = models.CharField(max_length=3, choices=DayChoices.choices, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.day)


class DoctorVendor(Vendor):
    doctor_name = models.CharField(max_length=100)
    working_days = models.CharField(max_length=100)
    video_consultation_fees = models.IntegerField(null=True, blank=True)
    clinic_visit_fees = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to='doc_image/', null=True, blank=True)

    def __str__(self):
        return f"{self.doctor_name}"


class PathologyVendor(Vendor):
    lab_name = models.CharField(max_length=100)
    working_days = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.establishment_name}"


class PhlebologistVendor(Vendor):
    registration_no = models.CharField(max_length=100)
    motorcycle_reg_no = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.establishment_name}"


class BloodBankVendor(Vendor):
    blood_bank_name = models.CharField(max_length=100)
    working_days = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.establishment_name}"


class PharmacyVendor(Vendor):
    days = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.establishment_name}"


class SlotTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    @staticmethod
    def create_slots(start_time_str, end_time_str):
        start_time = datetime.strptime(start_time_str, '%H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%H:%M:%S')
        current_time = start_time
        slots = []

        while current_time < end_time:
            end_slot_time = current_time + timedelta(minutes=10)
            if end_slot_time > end_time:
                break
            slot = SlotTime.objects.create(start_time=current_time.time(), end_time=end_slot_time.time())
            slots.append(slot)
            current_time = end_slot_time

        return slots

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}"


class Slot(models.Model):
    vendor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='vendor_user')
    slot_times = models.ManyToManyField(SlotTime)
    day = models.CharField(max_length=3, choices=DayChoices.choices)

    def __str__(self):
        return str(self.day)

    @classmethod
    def create_slots_for_days(cls, vendor, days_list, slots_timing):
        slots = []
        for day in days_list:
            slot = cls.objects.create(vendor=vendor, day=day)
            slot.slot_times.add(*slots_timing)
            slots.append(slot)
        return slots


class BookDoctorSlot(models.Model):
    customer = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="slot_taker")
    doctor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='slot_holder')
    accepted = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    booking_date = models.DateField(null=True, blank=True)
    meet_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=3, choices=DayChoices.choices, null=True, blank=True)
    service_type = models.CharField(choices=ServiceChoices.choices, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.doctor}"


class Review(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_reviews')
    vendor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='vendor_reviews')
    review = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vendor)
