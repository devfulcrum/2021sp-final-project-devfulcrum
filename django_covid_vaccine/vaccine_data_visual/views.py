from django.shortcuts import render
from django.http import JsonResponse
from .models import CovidData, VaccineData


def home_demo(request):
    return render(request, 'home_demo.html')


def covid_data_chart(request):
    print(request)
    labels = []
    data = []

    queryset = CovidData.objects.filter(country='Australia').order_by('date')
    for entry in queryset:
        labels.append(entry.date)
        data.append(entry.confirmed)

    return JsonResponse(data={
        'country': 'Australia Covid Cases',
        'labels': labels,
        'data': data,
    })


def vaccine_data_chart(request):
    print(request)
    labels = []
    data = []

    queryset = VaccineData.objects.filter(country='Australia').order_by('date')
    for entry in queryset:
        labels.append(entry.date)
        data.append(entry.doses_administered)

    return JsonResponse(data={
        'country': 'Australia Vaccine Doses Administered',
        'labels': labels,
        'data': data,
    })
