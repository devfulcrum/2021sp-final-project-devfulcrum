from environs import Env
from luigi import build

from final_project.etl.covid_data_confirmed_time_series_global import CovidDataConfirmedTimeSeriesGlobal
from final_project.etl.covid_data_confirmed_time_series_us import CovidDataConfirmedTimeSeriesUS
from final_project.etl.covid_data_deaths_time_series_global import CovidDataDeathsTimeSeriesGlobal
from final_project.etl.covid_data_deaths_time_series_us import CovidDataDeathsTimeSeriesUS
from final_project.etl.covid_data_recovered_time_series_global import CovidDataRecoveredTimeSeriesGlobal
from final_project.etl.covid_testing_data_time_series_us import CovidTestingData
from final_project.etl.tasks_covid_data import ByCountryCovid
from final_project.etl.tasks_vaccine_data import ByCountryVaccine, ByCountryMonthVaccine
from final_project.etl.vaccine_data_global import VaccineDataGlobal
from final_project.etl.vaccine_data_time_series_global import VaccineDataTimeSeriesGlobal

if __name__ == "__main__":
    env = Env()
    etl_url = env.str('VACCINE_GLOBAL_DATA_TIME_SERIES_URL')
    build([VaccineDataTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('VACCINE_GLOBAL_DATA_URL')
    build([VaccineDataGlobal(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('COVID_TESTING_DATA_URL')
    build([CovidTestingData(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('COVID_DATA_RECOVERED_TIME_SERIES_GLOBAL_URL')
    build([CovidDataRecoveredTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('COVID_DATA_DEATHS_TIME_SERIES_US_URL')
    build([CovidDataDeathsTimeSeriesUS(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('COVID_DATA_DEATHS_TIME_SERIES_GLOBAL_URL')
    build([CovidDataDeathsTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('COVID_DATA_CONFIRMED_TIME_SERIES_US_URL')
    build([CovidDataConfirmedTimeSeriesUS(etl_url=etl_url)], local_scheduler=True)
    etl_url = env.str('COVID_DATA_CONFIRMED_TIME_SERIES_GLOBAL_URL')
    build([CovidDataConfirmedTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True)
    build([ByCountryVaccine(subset=False)], local_scheduler=True)
    build([ByCountryMonthVaccine(subset=False)], local_scheduler=True)
    build([ByCountryCovid(subset=False)], local_scheduler=True)
