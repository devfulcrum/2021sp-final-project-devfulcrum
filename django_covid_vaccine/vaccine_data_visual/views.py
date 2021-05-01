from django.shortcuts import render
from django.http import JsonResponse
from .models import CovidData, VaccineData


def home_demo(request):
    """
    Template Function handles http request / response and HTML page rendering.

    :param request: gets the http request and returns response for rendering the HTML

    :return: render, html page response
    """

    return render(request, 'home_demo.html')


def covid_data_chart(request):
    """
    Handles http request and responds with formatted JSON data for covid for a given country

    :param request: http request

    :return: formatted JSON data response
    """

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
    """
    Handles http request and responds with formatted JSON data for vaccine for a given country

    :param request: http request

    :return: formatted JSON data response
    """

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
