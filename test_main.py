#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `final_project` package."""
from unittest import TestCase

from django.views.generic import TemplateView

from final_project.visual import linear_regression
from django.test import TestCase as DjangoTC
from datetime import datetime
from rest_framework.test import APIRequestFactory
from rest_framework import status

from vaccine_data_visual.api import CovidDataAPI, VaccineDataAPI
from vaccine_data_visual.models import CovidData, VaccineData
from vaccine_data_visual.views import home_demo, covid_data_chart, vaccine_data_chart, vaccine_covid_data_aggregation, \
    covid_cases_predict, vaccine_doses_predict, linear_reg_predict


class MainProjectLevelTests(TestCase):
    """
    Main project level tests are here.
    """
    def test_main(self):
        """
        This is just to have a main test that just performs a simple assert

        :return:

        """
        linear_regression.visual_demo()
        self.assertTrue(True)


class CovidDataTestCase(DjangoTC):

    def test_covid_data(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)


class VaccineDataTestCase(DjangoTC):

    def test_vaccine_data(self):
        date_now = datetime.now()
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)


class FinalProjectAPITestCase(DjangoTC):

    def test_covid_data_api(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        view = CovidDataAPI.as_view()
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/covid_data')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_vaccine_data_api(self):
        date_now = datetime.now()
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = VaccineDataAPI.as_view()
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/vaccine_data')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_home_demo(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = TemplateView.as_view(template_name="vaccine_data_visual/home_demo.html")
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/home_demo.html')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_home_angular(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = TemplateView.as_view(template_name="vaccine_data_visual/home_angular.html")
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/home_angular.html')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_home_chart(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = TemplateView.as_view(template_name="vaccine_data_visual/home_chart.html")
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/home_chart.html')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_home_lin_reg(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = TemplateView.as_view(template_name="vaccine_data_visual/home_lin_reg.html")
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/home_lin_reg.html')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_home_tf(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = TemplateView.as_view(template_name="vaccine_data_visual/home_tf.html")
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/home_tf.html')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_index(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        view = TemplateView.as_view(template_name="vaccine_data_visual/index.html")
        factory = APIRequestFactory()
        request = factory.get('/vaccine_data_visual/index.html')
        response = view(request)
        response.render()
        self.assertTrue(status.is_success(response.status_code))

    def test_view_covid_data_chart(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        factory = APIRequestFactory()
        request = factory.get('covid-data-chart')
        response = covid_data_chart(request)
        print(response)
        self.assertTrue(status.is_success(response.status_code))

    def test_view_vaccine_data_chart(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        factory = APIRequestFactory()
        request = factory.get('vaccine-data-chart')
        response = vaccine_data_chart(request)
        print(response)
        self.assertTrue(status.is_success(response.status_code))

    def test_view_vaccine_covid_data_aggregation(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        factory = APIRequestFactory()
        request = factory.get('vaccine-covid-data-aggregation')
        response = vaccine_covid_data_aggregation(request)
        print(response)
        self.assertTrue(status.is_success(response.status_code))

    def test_view_covid_cases_predict(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        factory = APIRequestFactory()
        request = factory.get('covid-cases-predict')
        response = covid_cases_predict(request)
        print(response)
        self.assertTrue(status.is_success(response.status_code))

    def test_view_vaccine_doses_predict(self):
        date_now = datetime.now()
        CovidData.objects.create(country="Australia", date=date_now, confirmed=10)
        covid_data = CovidData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, covid_data.date)
        self.assertTrue("Australia", covid_data.country)
        VaccineData.objects.create(country="Australia", date=date_now, doses_administered=1000)
        vaccine_data = VaccineData.objects.get(date=date_now, country="Australia")
        self.assertTrue(date_now, vaccine_data.date)
        self.assertTrue("Australia", vaccine_data.country)
        factory = APIRequestFactory()
        request = factory.get('vaccine-doses-predict')
        response = vaccine_doses_predict(request)
        print(response)
        self.assertTrue(status.is_success(response.status_code))

    def test_lin_reg(self):
        data = [[0, 1202], [1, 864], [2, 876], [3, 771], [4, 1479], [5, 1124], [6, 1368], [7, 1321], [8, 1292]]
        response = linear_reg_predict(data)
        self.assertEqual(response, [1400, 1451, 1502])
