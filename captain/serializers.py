from rest_framework import serializers
from captain.models import CaptainToken, Captain


class CaptainTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptainToken
        fields = '__all__'


class CaptainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Captain
        fields = '__all__'
