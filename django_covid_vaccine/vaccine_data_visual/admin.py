from django.contrib import admin

from .models import VaccineData, CovidData

admin.site.register(VaccineData)
admin.site.register(CovidData)
