"""django_covid_vaccine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from vaccine_data_visual import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'vaccine_data_visual/', include('vaccine_data_visual.urls')),
    path('covid-data-chart/', views.covid_data_chart, name='covid-data-chart'),
    path('vaccine-data-chart/', views.vaccine_data_chart, name='vaccine-data-chart'),
    path('vaccine-covid-data-aggregation/', views.vaccine_covid_data_aggregation,
         name='vaccine-covid-data-aggregation'),
    path('covid-cases-predict/', views.covid_cases_predict,
         name='covid-cases-predict'),
    path('vaccine-doses-predict/', views.vaccine_doses_predict,
         name='vaccine-doses-predict'),
]
