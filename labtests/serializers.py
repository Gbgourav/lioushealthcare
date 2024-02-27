from rest_framework import serializers
from .models import *


class HealthConcernSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthConcern
        fields = '__all__'


class HealthConcernSubCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.health_concern.image.url

    class Meta:
        model = HealthConcernSubCategory
        fields = ['name', 'uid', 'image', 'id']


class LabTestSerializer(serializers.ModelSerializer):
    vendor_uid = serializers.ReadOnlyField(source='vendor.uid')
    related_tests = serializers.SerializerMethodField()

    def get_related_tests(self, instance):
        return [{'name': related_test.name, 'uid': related_test.uid} for related_test in instance.related_tests.all()]

    class Meta:
        model = LabTest
        fields = '__all__'
