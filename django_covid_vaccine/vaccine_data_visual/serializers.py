from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import VaccineData, CovidData


class VaccineSerializer(ModelSerializer):
    class Meta:
        model = VaccineData
        fields = '__all__'


class CovidSerializer(ModelSerializer):
    class Meta:
        model = CovidData
        fields = '__all__'
