from django.core.management import BaseCommand
from django.db import transaction
import datetime

import pandas as pd
from pytz import timezone

from ...models import CovidData


class Command(BaseCommand):
    """
    Command class for loading covid data to sqlite database table.
    Works with data from the completed by ETL activities and further aggregates
    the data for reporting purpose.
    """

    help = "Load Covid data to covid_data table"

    def handle(self, *args, **options):
        """
        This function works with Covid Data that is available since Jan 22nd 2020.
        Loads the transformed data to covid_data table, leverages transaction.atomic.

        :param args: Nothing specifically defined for this function.

        :param options: Nothing specifically defined for this function.

        :return: None
        """

        est = timezone("EST")
        cur_date = datetime.datetime.now(est)
        print(cur_date)
        number_of_days = (
            cur_date - datetime.datetime.strptime("1/22/20", "%m/%d/%y").astimezone(est)
        ).days
        print(number_of_days)
        number_columns = list()
        for days in range(1, (number_of_days + 1)):
            number_columns.append(
                (datetime.datetime.now(est) - datetime.timedelta(days=days)).strftime(
                    "%#m/%#d/%y"
                )
            )
        df = pd.read_parquet(
            "../data/covid/subset-False/part.0.parquet", engine="pyarrow"
        )
        idx = ["Province/State", "Country/Region", "Lat", "Long"]
        melt_df = (
            pd.melt(df, id_vars=idx, value_vars=number_columns, var_name="Date")
            .sort_values(idx)
            .reset_index(drop=True)
        )
        print(melt_df)

        melt_df.drop(columns=["Province/State", "Lat", "Long"], inplace=True)
        melt_df.info()
        melt_df["Date"] = pd.to_datetime(melt_df["Date"])
        melt_df.info()
        melt_df.sort_values(["Country/Region", "Date"])
        new_df = melt_df.groupby(["Country/Region", "Date"]).sum()
        print(melt_df.groupby(["Country/Region", "Date"]).sum())
        print(new_df)
        print(new_df.to_string(index=True, max_rows=50))
        print(new_df.diff())
        new2_df = new_df.diff()
        print(new2_df)
        print(new2_df.to_string(index=True, max_rows=100))

        last_ten_days_date = datetime.datetime.now() - datetime.timedelta(days=10)
        print(last_ten_days_date)
        new3_df = new2_df[new2_df.index.get_level_values("Date") >= last_ten_days_date]
        print(new3_df)
        print(new3_df.to_string(index=True, max_rows=100))

        print(new3_df[new3_df.index.isin(["India"], level=0)])

        with transaction.atomic():
            covid_data = [
                CovidData(
                    country=idx[0],
                    date=idx[1],
                    confirmed=records["value"],
                )
                for idx, records in new3_df.iterrows()
            ]

            CovidData.objects.all().delete()
            CovidData.objects.bulk_create(covid_data)
