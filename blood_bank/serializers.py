from rest_framework import serializers
from .models import *


class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = '__all__'


class BloodTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodGroup
        fields = ['name', ]


class BloodBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBank
        fields = '__all__'


class BloodBankStockSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()

    def get_group_name(self, obj):
        return obj.group.name

    def get_type_name(self, obj):
        return obj.type.name

    class Meta:
        model = BloodBankStock
        fields = ['group_name', 'price', 'type_name', 'uid']
