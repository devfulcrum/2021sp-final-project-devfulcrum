from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from .api import CovidDataAPI, VaccineDataAPI

schema_view = get_schema_view(title="Final Project API")

urlpatterns = [
    url(r'^covid_data$', CovidDataAPI.as_view()),
    url(r'^vaccine_data$', VaccineDataAPI.as_view()),
    url(r'^home_chart', TemplateView.as_view(template_name="vaccine_data_visual/home_chart.html")),
    url(r'^home_angular', TemplateView.as_view(template_name="vaccine_data_visual/home_angular.html")),
    url(r'^home_demo', TemplateView.as_view(template_name="vaccine_data_visual/home_demo.html")),
    url(r'^index', TemplateView.as_view(template_name="vaccine_data_visual/index.html")),
    url(r'^home_tf', TemplateView.as_view(template_name="vaccine_data_visual/home_tf.html")),
    url(r'^home_lin_reg', TemplateView.as_view(template_name="vaccine_data_visual/home_lin_reg.html")),
]
