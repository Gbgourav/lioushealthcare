import json

from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import Vendor, BookDoctorSlot, BloodBankVendor
from .serializers import *
from django.http import JsonResponse

UserAccount = get_user_model()


class VendorCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        try:
            vendor_type = request.data.get('type')
            user = request.user
            start_day = request.data.get('start_day')
            end_day = request.data.get('end_day')
            end_time = request.data.get('end_time')
            start_time = request.data.get('start_time')
            if start_day and end_day:
                working_days = start_day + '-' + end_day
            if start_time and end_time:
                timing = start_time + '-' + end_time
            contact = request.data.get("contact")
            image = request.data.get("image")
            print("image", image)
            facilities_str = request.data.get("facilities")
            services_str = request.data.get("services")
            specialization_str = request.data.get("specialization")
            facilities = json.loads(facilities_str) if facilities_str else []
            services = json.loads(services_str) if services_str else []
            specialization = json.loads(specialization_str) if specialization_str else []
            address = request.data.get("address")
            pin_code = request.data.get("pin_code")
            establishment_name = request.data.get("establishment_name")
            state = request.data.get("state")
            state_obj = State.objects.filter(name=state).first()
            data_obj = None
            if vendor_type in ['Doctor', 'Pathology', 'Blood Bank']:
                if vendor_type == 'Doctor':
                    clinic_visit_fees = request.data.get("clinic_visit_fees")
                    doctor_name = request.data.get("doctor_name")
                    video_consultation_fees = request.data.get("video_consultation_fees")
                    data_obj = DoctorVendor.objects.create(user=user, working_days=working_days, timing=timing,
                                                           clinic_visit_fees=clinic_visit_fees, contact=contact,
                                                           doctor_name=doctor_name, image=image,
                                                           establishment_name=establishment_name,
                                                           address=address, pin_code=pin_code, state=state_obj,
                                                           video_consultation_fees=video_consultation_fees)
                    user.is_doctor = True

                elif vendor_type == 'Pathology':
                    lab_name = request.data.get("lab_name")

                    data_obj = PathologyVendor.objects.create(user=user, working_days=working_days, timing=timing,
                                                              contact=contact,
                                                              lab_name=lab_name,
                                                              establishment_name=establishment_name,
                                                              address=address, pin_code=pin_code, state=state_obj,
                                                              )
                    user.is_pathology = True

                elif vendor_type == 'Blood Bank':
                    blood_bank_name = request.data.get("blood_bank_name")

                    data_obj = BloodBankVendor.objects.create(user=user, working_days=working_days, timing=timing,
                                                              contact=contact,
                                                              blood_bank_name=blood_bank_name,
                                                              establishment_name=establishment_name,
                                                              address=address, pin_code=pin_code, state=state_obj,
                                                              )
                    user.is_blood_bank = True

                for service_name in services:
                    service_obj = Service.objects.filter(service_name=service_name).first()
                    if not service_obj:
                        service_obj = Service.objects.create(service_name=service_name)
                    data_obj.services.add(service_obj)

                for facility in facilities:
                    facility_obj = Facilities.objects.filter(facility_name=facility).first()
                    if not facility_obj:
                        facility_obj = Facilities.objects.create(facility_name=facility)
                    data_obj.facilities.add(facility_obj)

                for special in specialization:
                    special_obj = Specialization.objects.filter(specialization_name=special).first()
                    if not special_obj:
                        special_obj = Specialization.objects.create(specialization_name=special)
                    data_obj.specializations.add(special_obj)

                day_map = {
                    "Mon": 0,
                    "Tue": 1,
                    "Wed": 2,
                    "Thu": 3,
                    "Fri": 4,
                    "Sat": 5,
                    "Sun": 6,
                }

                start_day_number = day_map.get(start_day)
                end_day_number = day_map.get(end_day)
                days_diff = end_day_number - start_day_number
                days_list = []

                for i in range(days_diff + 1):
                    current_day_number = (start_day_number + i) % 7
                    current_day_name = list(day_map.keys())[list(day_map.values()).index(current_day_number)]
                    days_list.append(current_day_name)

                for day in days_list:
                    start = datetime.strptime(start_time, '%H:%M:%S')
                    end = datetime.strptime(end_time, '%H:%M:%S')
                    time_obj = Timing.objects.get_or_create(vendor=request.user, day=day, start_time=start,
                                                            end_time=end)

                slots_timing = SlotTime.create_slots(start_time, end_time)
                slots = Slot.create_slots_for_days(request.user, days_list, slots_timing)

                for slot in slots:
                    print(slot)
                    slot.save()

            elif vendor_type == 'Pharmacy':
                data_obj = PharmacyVendor.objects.create(user=user,
                                                         contact=contact,
                                                         establishment_name=establishment_name,
                                                         address=address, pin_code=pin_code, state=state_obj,
                                                         )
                user.is_pharmacy = True

            user.is_profile_completed = True
            user.save()

            return JsonResponse({"success": True, "message": "Account details added successfully!"})


        except Exception as e:
            print("e", str(e))
            return JsonResponse({"success": False, "message": str(e)})


class BookDoctorSlotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id')
        date = request.data.get('date')
        time = request.data.get('time')
        user = request.user

        doctor = DoctorVendor.objects.get(uid=doctor_id)

        if BookDoctorSlot.objects.filter(created_at=date, booking_time=time).exists():
            return JsonResponse({"success": False, "message": "This slot is already taken"})

        slot = BookDoctorSlot.objects.create(customer=user, doctor=doctor, booking_time=time)

        return JsonResponse({"success": True, "message": "Slot created successfully", "data": slot.data})


class GetVendorProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user

            if user.is_doctor:
                doctor_obj = DoctorVendor.objects.get(user__email=user.email)
                data = DoctorVendorSerializer(doctor_obj).data

                return JsonResponse({"success": True, "data": data})

            elif user.is_blood_bank:
                obj = BloodBankVendor.objects.get(user__email=user.email)
                data = BloodBankVendorSerializer(obj).data

                return JsonResponse({"success": True, "data": data})

            elif user.is_pharmacy:
                obj = PharmacyVendor.objects.get(user__email=user.email)
                data = PharmacyVendorSerializer(obj).data
                return JsonResponse({'success': True, "data": data})

        except Exception as e:
            print(str(e))
            return JsonResponse({"success": False, "message": str(e)})
