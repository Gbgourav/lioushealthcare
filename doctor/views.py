from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from doctor.models import DoctorType
from doctor.serializers import DoctorTypeSerializer
from rest_framework import viewsets, generics

from labtests.models import LabTest
from labtests.serializers import LabTestSerializer
from vendor.models import DoctorVendor, Slot, BookDoctorSlot, Review, Timing, PathologyVendor, Service, Specialization, \
    Facilities, Vendor
from vendor.serializers import DoctorVendorSerializer, SlotSerializer, ReviewSerializer, TimingSerializer, \
    BookDoctorSlotSerializer, ServiceSerializer, SpecializationsSerializer, FacilitiesSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

UserAccount = get_user_model()


class DoctorTypeListView(ListAPIView):
    queryset = Specialization.objects.all().order_by('specialization_name')
    serializer_class = DoctorTypeSerializer


class DoctorVendorViewSet(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            uid = self.kwargs.get('uid')
            doc_list = DoctorVendor.objects.filter(specializations__uid__exact=uid)
            print("doc_list", doc_list)
            serializer = DoctorVendorSerializer(doc_list, many=True).data
            return JsonResponse({'success': True, 'data': serializer})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


class SlotListAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        uid = self.kwargs.get('uid')
        date = self.kwargs.get('date')
        type = self.kwargs.get('type')
        if type == 'labtest':
            doctor = PathologyVendor.objects.filter(uid=uid).first()
        else:
            doctor = DoctorVendor.objects.filter(uid=uid).first()
        date_object = datetime.strptime(date, "%Y-%m-%d")
        day_of_week_string = date_object.strftime("%a")

        slot_available = BookDoctorSlot.objects.filter(doctor=doctor.user, booking_date=date,
                                                       day=day_of_week_string).values_list('start_time',
                                                                                           flat=True)
        vendor = Slot.objects.filter(vendor=doctor.user, day=day_of_week_string)
        serialized_value = SlotSerializer(vendor, many=True, context={'slot_available': slot_available,
                                                                      'day_of_week_string': day_of_week_string,
                                                                      'vendor': doctor.user}).data

        return JsonResponse({'data': serialized_value, 'success': True})


class DoctorProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        uid = self.kwargs.get('uid')
        doctor = DoctorVendor.objects.filter(uid=uid).first()
        doctor_data = DoctorVendorSerializer(doctor).data
        reviews = Review.objects.filter(vendor=doctor.user)
        timings = Timing.objects.filter(vendor=doctor.user)
        customer_review = ReviewSerializer(reviews, many=True).data
        doctor_timings = TimingSerializer(timings, many=True).data
        return JsonResponse(
            {'doctor_data': doctor_data, 'customer_review': customer_review, 'doctor_timings': doctor_timings,
             'success': True})


class GetInitialDataView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            services = Service.objects.filter()
            specialization = Specialization.objects.filter()
            facilities = Facilities.objects.filter()
            services_data = ServiceSerializer(services, many=True).data
            facilities_data = FacilitiesSerializer(facilities, many=True).data
            specialization_data = SpecializationsSerializer(specialization, many=True).data

            return JsonResponse(
                {'services_data': services_data, 'specialization_data': specialization_data,
                 'facilities_data': facilities_data, 'success': True})

        except Exception as e:
            print("Exception: ", str(e))
            return JsonResponse({'success': True, 'message': str(e)})


class ConfirmSlot(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctor_id = self.request.query_params.get('doctor_id')
        service_type = self.request.query_params.get('service_type')
        date = self.request.query_params.get('date')
        slot_start = self.request.query_params.get('slot_start')
        type = self.request.query_params.get('type')
        slot_end = self.request.query_params.get('slot_end')
        if type == 'labtest':
            doctor = PathologyVendor.objects.filter(uid=doctor_id).first()
        else:
            doctor = DoctorVendor.objects.filter(uid=doctor_id).first()

        if BookDoctorSlot.objects.filter(doctor=doctor.user, booking_date=date, start_time=slot_start,
                                         end_time=slot_end).exists():
            return JsonResponse({'success': False, 'message': 'Slot Already Booked'})

        if type == 'labtest':
            doctor = LabTest.objects.get(vendor=doctor, uid=service_type)
            doc_data = LabTestSerializer(doctor).data
        else:
            doctor = DoctorVendor.objects.get(uid=doctor_id)
            doc_data = DoctorVendorSerializer(doctor).data

        if type == 'labtest':
            fees = doctor.price
            texes = fees * 18 / 100
            total_fees = fees + texes
        else:
            if service_type == 'video':
                fees = doctor.video_consultation_fees
                texes = fees * 18 / 100
                total_fees = fees + texes
            else:
                fees = doctor.clinic_visit_fees
                texes = fees * 18 / 100
                total_fees = fees + texes

        return JsonResponse(
            {'success': True, 'fees': fees, 'texes': texes, 'total_fees': total_fees, 'doctor': doc_data})


class Payment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            doctor_id = self.request.data.get('doctor_id')
            service_type = self.request.data.get('service_type')
            date = self.request.data.get('date')
            slot_start = self.request.data.get('slot_start')
            slot_end = self.request.data.get('slot_end')
            type = self.request.data.get('type')
            date_object = datetime.strptime(date, "%Y-%m-%d")
            day_of_week_string = date_object.strftime("%a")
            user = request.user
            if type == 'labtest':
                doctor = PathologyVendor.objects.filter(uid=doctor_id).first()
            else:
                doctor = DoctorVendor.objects.filter(uid=doctor_id).first()
            if service_type == 'video':
                service = 'Video Consultation'
            else:
                service = 'Clinic Visit'

            booked_slot = BookDoctorSlot.objects.create(
                doctor=doctor.user,
                customer=user,
                start_time=slot_start,
                end_time=slot_end,
                day=day_of_week_string,
                service_type=service,
                booking_date=date
            )

            slot_data = BookDoctorSlotSerializer(booked_slot).data

            return JsonResponse({'success': True, 'data': slot_data})

        except Exception as e:
            print("Error", e)
            return JsonResponse({'success': False, 'message': str(e)})


class BookDoctorSlotAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            approved_set = BookDoctorSlot.objects.filter(accepted=True, doctor__exact=user)
            pending_set = BookDoctorSlot.objects.filter(accepted=False, doctor=user)
            cancelled_set = BookDoctorSlot.objects.filter(is_canceled=True, doctor=user)

            approved = BookDoctorSlotSerializer(approved_set, many=True).data
            pending = BookDoctorSlotSerializer(pending_set, many=True).data
            cancelled = BookDoctorSlotSerializer(cancelled_set, many=True).data

            return JsonResponse({'success': True, 'approved': approved, 'pending': pending, 'cancelled': cancelled})

        except Exception as e:
            print("Error", e)
            return JsonResponse({'success': False, 'message': str(e)})
