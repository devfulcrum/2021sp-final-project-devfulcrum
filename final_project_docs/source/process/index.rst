===================================
Processing
===================================


Project Data
================================

- Aggregated daily by Johns Hopkins University and published to GitHub repo

- Data Files formats varies over time and based on the origin

- Not all data files are available at the same

- Run daily / nightly scheduled jobs to pull the data files

- Download all the files for use, currently use covid cases and vaccination time series data

- Transform the data for consistency and downstream use

Data Analysis
================================

The code analysis leverages both data files pull from GitHub repo, conduct analysis
transform the data for database load and then load the data to the database for
visualization and models execution

.. code-block::

    def perform_analysis(self, analysis_dataframe):
        """Performs actual computation of confirmed cases by country.
        Args:
            analysis_dataframe: Covid data
        Returns:
            dataframe that contains the calculated results
        """
        analysis_dataframe["Country"] = analysis_dataframe["Country/Region"]
        analysis_dataframe["Confirmed"] = analysis_dataframe[
            (datetime.datetime.now() - datetime.timedelta(days=2)).strftime(
                "%-m/%-d/%y"
            )
        ].astype(int)
        return (
            analysis_dataframe.groupby("Country")
            .Confirmed.sum()
            .round()
            .astype(int)
            .to_frame()
        )

The data files require aggregation and transformation

.. code-block::

        melt_df = (
            pd.melt(df, id_vars=idx, value_vars=number_columns, var_name="Date")
            .sort_values(idx)
            .reset_index(drop=True)
        )
        melt_df.groupby(["Country/Region", "Date"]).sum()


Load the data to the database for visualization

.. code-block::

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
