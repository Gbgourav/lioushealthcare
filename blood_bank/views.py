from decimal import Decimal
import random
from django.db import transaction
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from blood_bank.models import *
from blood_bank.serializers import BloodTypeSerializer, BloodBankSerializer, BloodBankStockSerializer


class BloodBankDashboardAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            types = BloodGroup.objects.all()
            types_data = BloodTypeSerializer(types, many=True).data
            all_blood_banks = BloodBank.objects.all()
            few_banks = random.sample(list(all_blood_banks), min(5, len(all_blood_banks)))
            bank_data = BloodBankSerializer(few_banks, many=True).data
            return JsonResponse({'success': True, "types_data": types_data, "bank_data": bank_data})

        except Exception as e:
            return JsonResponse({'success': False, "error": str(e)})


class BloodBankGroupAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            uid = self.request.query_params.get('uid')
            get_banks = BloodBankStock.objects.filter(group__uid=uid).values('bank__uid').distinct()
            get_all_banks = BloodBank.objects.filter(uid__in=get_banks)
            bank_data = BloodBankSerializer(get_all_banks, many=True).data
            return JsonResponse({'success': True, "bank_data": bank_data})

        except Exception as e:
            return JsonResponse({'success': False, "error": str(e)})


class BloodBankDataAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            uid = self.request.query_params.get('uid')
            get_banks = BloodBank.objects.filter(uid=uid).first()
            stock_1 = BloodBankStock.objects.filter(bank__uid=uid, type__name='Cryoprotectant (CRYO)')
            stock_2 = BloodBankStock.objects.filter(bank__uid=uid, type__name='Platelet Concentrate (PC)')
            stock_3 = BloodBankStock.objects.filter(bank__uid=uid, type__name='Fresh Frozen Plasma (FFP)')
            stock_4 = BloodBankStock.objects.filter(bank__uid=uid, type__name='Whole Blood (WB)')
            bank_data = BloodBankSerializer(get_banks).data
            stock_data_1 = BloodBankStockSerializer(stock_1, many=True).data
            stock_data_2 = BloodBankStockSerializer(stock_2, many=True).data
            stock_data_3 = BloodBankStockSerializer(stock_3, many=True).data
            stock_data_4 = BloodBankStockSerializer(stock_4, many=True).data
            return JsonResponse(
                {'success': True, "bank_data": bank_data, 'stock_data_1': stock_data_1, 'stock_data_2': stock_data_2,
                 'stock_data_3': stock_data_3, 'stock_data_4': stock_data_4})

        except Exception as e:
            return JsonResponse({'success': False, "error": str(e)})


@api_view(['POST'])
@transaction.atomic
def add_unique_uids(request):
    try:
        all_type = BloodType.objects.all()
        for bank in all_type:
            all_bloods = BloodGroup.objects.all()
            for blood in all_bloods:
                if blood == 'A+' or blood == 'A-':
                    price = Decimal(400)
                elif blood == 'B-' or blood == 'B+':
                    price = Decimal(500)
                else:
                    price = Decimal(1000)
                bacnk_name = BloodBank.objects.all()

                for bacnk in bacnk_name:
                    bl = BloodBankStock.objects.create(bank=bacnk, group=blood, type=bank, price=price)

    except Exception as e:
        print(str(e))
        return Response({"error": "Failed to add UUIDs. IntegrityError occurred."}, status=500)
