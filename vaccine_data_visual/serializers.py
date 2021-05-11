from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import VaccineData, CovidData


class VaccineSerializer(ModelSerializer):
    """
    VaccineData serializer for REST API Integration
    """

    class Meta:
        model = VaccineData
        fields = '__all__'


class CovidSerializer(ModelSerializer):
    """
    CovidData serializer for REST API Integration
    """

    class Meta:
        model = CovidData
        fields = '__all__'
