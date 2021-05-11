from rest_framework.generics import ListAPIView

from .serializers import CovidSerializer, VaccineSerializer
from .models import CovidData, VaccineData


class CovidDataAPI(ListAPIView):
    queryset = CovidData.objects.all()
    serializer_class = CovidSerializer


class VaccineDataAPI(ListAPIView):
    queryset = VaccineData.objects.all()
    serializer_class = VaccineSerializer
