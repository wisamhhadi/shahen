from rest_framework import serializers
from mandob.models import MandobToken, Mandob


class MandobTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MandobToken
        fields = '__all__'


class MandobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mandob
        fields = '__all__'
