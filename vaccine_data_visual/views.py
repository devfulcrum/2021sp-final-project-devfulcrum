from django.shortcuts import render
from django.http import JsonResponse
from .models import CovidData, VaccineData
import numpy as np
from sklearn.linear_model import LinearRegression


def home_demo(request):
    """
    Template Function handles http request / response and HTML page rendering.

    :param request: gets the http request and returns response for rendering the HTML

    :return: render, html page response
    """

    return render(request, "home_demo.html")


def covid_data_chart(request):
    """
    Handles http request and responds with formatted JSON data for covid for a given country

    :param request: http request

    :return: formatted JSON data response
    """

    print(request)
    labels = []
    data = []

    queryset = CovidData.objects.filter(country="Australia").order_by("date")
    for entry in queryset:
        labels.append(entry.date)
        data.append(entry.confirmed)

    return JsonResponse(
        data={
            "country": "Australia Covid Cases",
            "labels": labels,
            "data": data,
        }
    )


def vaccine_data_chart(request):
    """
    Handles http request and responds with formatted JSON data for vaccine for a given country

    :param request: http request

    :return: formatted JSON data response
    """

    print(request)
    labels = []
    data = []

    queryset = VaccineData.objects.filter(country="Australia").order_by("date")
    for entry in queryset:
        labels.append(entry.date)
        data.append(entry.doses_administered)

    return JsonResponse(
        data={
            "country": "Australia Vaccine Doses Administered",
            "labels": labels,
            "data": data,
        }
    )


def vaccine_covid_data_aggregation(request):
    print(request)
    country = []
    labels = []
    data_vaccine = []
    data_covid = []

    queryset_covid = CovidData.objects.all().order_by("country")
    for covid_entry in queryset_covid:
        country.append(covid_entry.country)
        labels.append(covid_entry.date)
        data_covid.append(covid_entry.confirmed)
        queryset_vaccine = VaccineData.objects.filter(
            country=covid_entry.country, date=covid_entry.date
        ).order_by("country")
        if queryset_vaccine.exists():
            for vaccine_entry in queryset_vaccine:
                data_vaccine.append(vaccine_entry.doses_administered)
        else:
            data_vaccine.append(0)

    return JsonResponse(
        data={
            "country": country,
            "labels": labels,
            "data_covid": data_covid,
            "data_vaccine": data_vaccine,
        }
    )


def covid_cases_predict(request):
    """

    http request to perform covid cases linear regression prediction

    :param request: http request to perform covid cases linear regression prediction

    :return: JSON data of predicted values

    """

    print(request)
    data_cases = []
    country_predict_cases = []
    country = ""
    i = 0

    queryset_covid = CovidData.objects.all().order_by("country")
    for covid_entry in queryset_covid:
        if country != covid_entry.country:
            if country != "":
                print(data_cases)
                predict_cases = linear_reg_predict(data_cases)
                predict_cases.append(country)
                print(predict_cases)
                country_predict_cases.append(predict_cases)
                i = 0
                data_cases.clear()
            country = covid_entry.country
        data_cases.append([i, covid_entry.confirmed])
        i = i + 1

    return JsonResponse(
        data={
            "country_predict_cases": country_predict_cases,
        }
    )


def vaccine_doses_predict(request):
    """

    http request to perform covid cases linear regression prediction

    :param request: http request to perform vaccine doses linear regression prediction

    :return: JSON data of predicted values

    """

    print(request)
    vaccine_doses = []
    country_predict_doses = []
    country = ""
    i = 0

    queryset_vaccine = VaccineData.objects.all().order_by("country")
    for vaccine_entry in queryset_vaccine:
        if country != vaccine_entry.country:
            if country != "":
                print(vaccine_doses)
                predict_doses = linear_reg_predict(vaccine_doses)
                predict_doses.append(country)
                print(predict_doses)
                country_predict_doses.append(predict_doses)
                i = 0
                vaccine_doses.clear()
            country = vaccine_entry.country
        vaccine_doses.append([i, vaccine_entry.doses_administered])
        i = i + 1

    return JsonResponse(
        data={
            "country_predict_doses": country_predict_doses,
        }
    )


def linear_reg_predict(data):
    """

    Perform linear regression model execution and return the predicted values

    :param data: data sequence (covid or vaccine data for given country)

    :return:
        The generated predicted values for the next few days

    """

    X = np.array(data)[:, 0].reshape(-1, 1)
    y = np.array(data)[:, 1].reshape(-1, 1)

    to_predict_x = [len(data), len(data) + 1, len(data) + 2]
    to_predict_x = np.array(to_predict_x).reshape(-1, 1)

    lin_reg = LinearRegression()
    lin_reg.fit(X, y)

    predicted_y = lin_reg.predict(to_predict_x)
    m = lin_reg.coef_
    c = lin_reg.intercept_
    print("Predicted y:\n", predicted_y)
    print("slope (m): ", m)
    print("y-intercept (c): ", c)
    day1 = [round(num) for num in predicted_y[0]][0]
    day2 = [round(num) for num in predicted_y[1]][0]
    day3 = [round(num) for num in predicted_y[2]][0]
    day1 = day1 if day1 >= 0 else 0
    day2 = day2 if day2 >= 0 else 0
    day3 = day3 if day3 >= 0 else 0
    rounded_predict = [day1, day2, day3]

    return rounded_predict
