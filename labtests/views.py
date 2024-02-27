import random
import string

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from labtests.models import HealthConcern, HealthConcernSubCategory, LabTest
from labtests.serializers import HealthConcernSerializer, HealthConcernSubCategorySerializer, LabTestSerializer


# Create your views here.


class GetProductListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            concern = HealthConcern.objects.filter()
            health_checkups = HealthConcernSubCategory.objects.filter(health_concern__name='Health Checkups')
            women_health = HealthConcernSubCategory.objects.filter(health_concern__name='Women’s Health')
            men_health = HealthConcernSubCategory.objects.filter(health_concern__name='Men’s Health')
            elderly_care = HealthConcernSubCategory.objects.filter(health_concern__name='Elderly Care')
            tests_by_organs = HealthConcernSubCategory.objects.filter(health_concern__name='Tests by Organs')
            concern_data = HealthConcernSerializer(concern, many=True).data
            health_checkups_data = HealthConcernSubCategorySerializer(health_checkups, many=True).data
            women_health_data = HealthConcernSubCategorySerializer(women_health, many=True).data
            men_health_data = HealthConcernSubCategorySerializer(men_health, many=True).data
            elderly_care_data = HealthConcernSubCategorySerializer(elderly_care, many=True).data
            tests_by_organs_data = HealthConcernSubCategorySerializer(tests_by_organs, many=True).data
            return JsonResponse(
                {'success': True, 'concern_data': concern_data, 'health_checkups_data': health_checkups_data,
                 'women_health_data': women_health_data, 'men_health_data': men_health_data,
                 'elderly_care_data': elderly_care_data, 'tests_by_organs_data': tests_by_organs_data})
        except Exception as e:
            print("Exception: ", str(e))
            return JsonResponse({'success': False, 'message': (str(e))})


class GetLabListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            uid = request.query_params.get('uid')
            lab_list = LabTest.objects.filter(sub_category__uid=uid).all()
            lab_list_data = LabTestSerializer(lab_list, many=True).data

            return JsonResponse({'success': True, 'lab_list': lab_list_data})

        except Exception as e:
            print("Exception: ", str(e))
            return JsonResponse({'success': False, 'message': (str(e))})


class Payment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # class TestOrder(models.Model):
    #     user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='test_user')
    #     payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payments_for_test', null=True,
    #                                 blank=True)
    #     test = models.ForeignKey(LabCart, on_delete=models.CASCADE, related_name='test_product', null=True, blank=True)
    #     uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    #     is_delivered = models.BooleanField(default=False)
    #     is_cancelled = models.BooleanField(default=False)
    #     delivered_data = models.DateTimeField(null=True, blank=True)
    #     created = models.DateTimeField(auto_now_add=True)
    #     updated = models.DateTimeField(auto_now=True)
    #
    #     def __str__(self):
    #         return str(self.user)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         doctor_id = self.request.data.get('doctor_id')
    #         service_type = self.request.data.get('service_type')
    #         date = self.request.data.get('date')
    #         slot_start = self.request.data.get('slot_start')
    #         slot_end = self.request.data.get('slot_end')
    #         type = self.request.data.get('type')
    #         date_object = datetime.strptime(date, "%Y-%m-%d")
    #         day_of_week_string = date_object.strftime("%a")
    #         user = request.user
    #         if type == 'labtest':
    #             doctor = PathologyVendor.objects.filter(uid=doctor_id).first()
    #         else:
    #             doctor = DoctorVendor.objects.filter(uid=doctor_id).first()
    #         if service_type == 'video':
    #             service = 'Video Consultation'
    #         else:
    #             service = 'Clinic Visit'
    #
    #         booked_slot = BookDoctorSlot.objects.create(
    #             doctor=doctor.user,
    #             customer=user,
    #             start_time=slot_start,
    #             end_time=slot_end,
    #             day=day_of_week_string,
    #             service_type=service,
    #             booking_date=date
    #         )
    #
    #         slot_data = BookDoctorSlotSerializer(booked_slot).data
    #
    #         return JsonResponse({'success': True, 'data': slot_data})
    #
    #     except Exception as e:
    #         print("Error", e)
    #         return JsonResponse({'success': False, 'message': str(e)})


class adddataapu(APIView):
    def post(self, request):
        lab_list = LabTest.objects.filter().all()
        for lab in lab_list:
            random_text = 'Tower4 New delhi'
            lab.address = random_text
            lab.save()
