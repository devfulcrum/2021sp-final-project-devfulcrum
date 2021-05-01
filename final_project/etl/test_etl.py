from unittest import TestCase
from environs import Env
from luigi import build
from final_project.etl.covid_data_confirmed_time_series_global import CovidDataConfirmedTimeSeriesGlobal
from final_project.etl.covid_data_confirmed_time_series_us import CovidDataConfirmedTimeSeriesUS
from final_project.etl.covid_data_deaths_time_series_global import CovidDataDeathsTimeSeriesGlobal
from final_project.etl.covid_data_deaths_time_series_us import CovidDataDeathsTimeSeriesUS
from final_project.etl.covid_data_recovered_time_series_global import CovidDataRecoveredTimeSeriesGlobal
from final_project.etl.covid_testing_data_time_series_us import CovidTestingData
from final_project.etl.tasks_covid_data import ByCountryCovid, ByCountryMonthCovid
from final_project.etl.tasks_vaccine_data import ByCountryVaccine, ByCountryMonthVaccine
from final_project.etl.vaccine_data_global import VaccineDataGlobal
from final_project.etl.vaccine_data_time_series_global import VaccineDataTimeSeriesGlobal


class ETLTests(TestCase):
    """
    This class contains all the tests for ETL activities (Luigi Tasks and Dask)

    """

    def test_etl(self):
        """
        This is just to have a main test that just performs a simple assert

        :return:

        """
        self.assertTrue(True)

    def test_vaccine_data_time_series_global(self):
        """
        This performs vaccine data time series test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('VACCINE_GLOBAL_DATA_TIME_SERIES_URL')
        self.assertTrue(build([VaccineDataTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True))

    def test_vaccine_data_global(self):
        """
        This performs vaccine data global test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('VACCINE_GLOBAL_DATA_URL')
        self.assertTrue(build([VaccineDataGlobal(etl_url=etl_url)], local_scheduler=True))

    def test_covid_testing_data(self):
        """
        This performs covid testing data test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('COVID_TESTING_DATA_URL')
        self.assertTrue(build([CovidTestingData(etl_url=etl_url)], local_scheduler=True))

    def test_covid_data_recovered_time_series_global(self):
        """
        This performs covid data recovered time series global test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('COVID_DATA_RECOVERED_TIME_SERIES_GLOBAL_URL')
        self.assertTrue(build([CovidDataRecoveredTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True))

    def test_covid_data_deaths_time_series_us(self):
        """
        This performs covid data deaths time series US test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('COVID_DATA_DEATHS_TIME_SERIES_US_URL')
        self.assertTrue(build([CovidDataDeathsTimeSeriesUS(etl_url=etl_url)], local_scheduler=True))

    def test_covid_data_deaths_time_series_global(self):
        """
        This performs covid data deaths time series global test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('COVID_DATA_DEATHS_TIME_SERIES_GLOBAL_URL')
        self.assertTrue(build([CovidDataDeathsTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True))

    def test_covid_data_confirmed_time_series_us(self):
        """
        This performs covid data confirmed time series US test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('COVID_DATA_CONFIRMED_TIME_SERIES_US_URL')
        self.assertTrue(build([CovidDataConfirmedTimeSeriesUS(etl_url=etl_url)], local_scheduler=True))

    def test_covid_data_confirmed_time_series_global(self):
        """
        This performs covid data confirmed time series global test for luigi task

        :return:

        """
        env = Env()
        etl_url = env.str('COVID_DATA_CONFIRMED_TIME_SERIES_GLOBAL_URL')
        self.assertTrue(build([CovidDataConfirmedTimeSeriesGlobal(etl_url=etl_url)], local_scheduler=True))

    def test_aggregation(self):
        """
        This performs vaccine and covid data aggregation test

        :return:

        """
        self.assertTrue(build([ByCountryVaccine(subset=False)], local_scheduler=True))
        self.assertTrue(build([ByCountryMonthVaccine(subset=False)], local_scheduler=True))
        self.assertTrue(build([ByCountryCovid(subset=False)], local_scheduler=True))
        self.assertTrue(build([ByCountryMonthCovid(subset=False)], local_scheduler=True))
