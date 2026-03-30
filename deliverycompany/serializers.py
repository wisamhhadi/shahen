from rest_framework import serializers
from deliverycompany.models import DeliveryCompanyToken, DeliveryCompany


class DeliveryCompanyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCompanyToken
        fields = '__all__'


class DeliveryCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCompany
        fields = '__all__'
