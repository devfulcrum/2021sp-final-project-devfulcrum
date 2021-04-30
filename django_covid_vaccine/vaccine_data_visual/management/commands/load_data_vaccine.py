from django.core.management import BaseCommand
from django.db import transaction
import datetime

import pandas as pd

from ...models import VaccineData


class Command(BaseCommand):
    help = "Load Covid and Vaccine data"

    def handle(self, *args, **options):
        df = pd.read_parquet('../data/vaccine/subset-False/part.0.parquet', engine='pyarrow')
        df.drop(columns=['People_partially_vaccinated', 'People_fully_vaccinated', 'Report_Date_String', 'UID'], inplace=True)
        df.info()
        df['Date'] = pd.to_datetime(df['Date'])
        df.info()
        df.reset_index(drop=True, inplace=True)
        df = df.set_index(['Country_Region', 'Date'])
        df.sort_values(['Country_Region', 'Date'])
        df['Doses_admin'] = pd.to_numeric(df['Doses_admin'])
        new_df = df.groupby(['Country_Region', 'Date']).sum()
        print(df.groupby(['Country_Region', 'Date']).sum())
        print(new_df)
        print(new_df.to_string(index=True, max_rows=50))
        print(new_df.diff())
        new2_df = new_df.diff()
        print(new2_df)
        print(df)
        print(df.diff())
        new2_df = df.diff()
        print(new2_df)
        print(new2_df.to_string(index=True, max_rows=100))

        last_ten_days_date = datetime.datetime.now() - datetime.timedelta(days=10)
        print(last_ten_days_date)
        new3_df = new2_df[new2_df.index.get_level_values('Date') >= last_ten_days_date]
        print(new3_df)
        print(new3_df.to_string(index=True, max_rows=100))

        print(new3_df[new3_df.index.isin(['India'], level=0)])

        with transaction.atomic():
            covid_data = [
                VaccineData(
                    country=idx[0],
                    date=idx[1],
                    doses_administered=records["Doses_admin"],
                )
                for idx, records in new3_df.iterrows()
            ]

            VaccineData.objects.all().delete()
            VaccineData.objects.bulk_create(covid_data)
