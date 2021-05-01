import datetime
import logging
import os

from csci_utils.luigi.dask.target import CSVTarget, ParquetTarget
from luigi import ExternalTask, Task, BoolParameter
from luigi import Parameter
from csci_utils.luigi.target.task import (
    Requires,
    Requirement,
    TargetOutput,
)
from pytz import timezone

os.environ["TZ"] = "US/Eastern"
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p %Z",
)


class CovidDataGlobalTask(ExternalTask):
    """Luigi ExternalTask to work with GIT CSVTarget. All three default variables
    (git_root, git_glob and git_ext) can be overridden.  The default values are used
    for working with a specific GIT download.  I have overridden them for test cases to work with
    local mock data.

    Parameters:
        git_root: str, git root directory path
        git_glob: str, glob of data file names
        git_ext: str, extension will be added to the glob

    Outputs:
        Returns a CSVTarget instance
    """

    # default parameters
    git_root = Parameter(
        default="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
    )
    git_glob = Parameter(default="time_series_covid19_confirmed_global")
    git_ext = Parameter(default=".csv")

    # output functions uses this variable to return CSVTarget instance
    output = TargetOutput(
        "{task.git_root}",
        ext="{task.git_ext}",
        target_class=CSVTarget,
        glob="{task.git_glob}",
        flag=None,
        storage_options=None,
    )


class CovidDataGlobalCleanupTask(Task):
    """Luigi Task to clean Covid time series data. The input is from
    External Task that specifies files in GIT. The cleaning from below code handles
    removing rows with null date and confirmed cases values are non-zero.
    The default parameters can be overridden for testing and I have overridden for
    all test cases.

    Parameters:
        subset: bool, True to process one partition, False to process the entire dataset
                    default: True
        data_root: str, base directory to store cleaned output files

    Output:
        Dataframe stored in compressed Parquet format

    """

    # default parameters
    subset = BoolParameter(default=True)
    data_root = Parameter(default="./data/covid/")

    # External task completion is required, to work with GIT / CSVTarget
    requires = Requires()
    input_data = Requirement(CovidDataGlobalTask)

    # TargetOutput returns ParquetTarget
    output = TargetOutput(
        "{task.data_root}",
        ext="subset-{task.subset}/",
        target_class=ParquetTarget,
        flag="_SUCCESS",
        storage_options=None,
    )

    def run(self):
        """
        Clean Covid data from Task input and stores dataframe in Parquet format.

        :return:
            File content is stored in the data directory
        """

        # The columns [460 plus date data column contains confirmed covid cases numbers]
        # are all integers. However, given there are missing values, you must first
        # read them as floats, fill nan's as 0, then convert to int.
        # You can provide a dict of {col: dtype} when providing the dtype arg in places like
        # read_parquet and astype.
        est = timezone("EST")
        cur_date = datetime.datetime.now(est)
        logging.info(cur_date)
        number_of_days = (
            cur_date - datetime.datetime.strptime("1/22/20", "%m/%d/%y").astimezone(est)
        ).days
        logging.info(number_of_days)
        number_columns = list()
        for days in range(1, (number_of_days + 1)):
            number_columns.append(
                (datetime.datetime.now(est) - datetime.timedelta(days=days)).strftime(
                    "%-m/%-d/%y"
                )
            )
        logging.info(number_columns)
        # Ensure that the date column is parsed as a pandas datetime using parse_dates
        cdg_dask = self.input()["input_data"].read_dask(
            dtype={c: "float" for c in number_columns}
        )

        if self.subset:
            cdg_dask = cdg_dask.get_partition(0)

        # perform data cleaning
        # Remove any blank countries
        cdg_dask = cdg_dask[~cdg_dask[cdg_dask.columns[1]].isnull()]

        # You should set the index to Country_Region and ensure the output reads back with meaningful divisions
        # vdg_dask = vdg_dask.set_index("Country_Region")
        cdg_dask[number_columns] = cdg_dask[number_columns].fillna(0).astype(int)

        # write_dask parquet file output with gzip compression.
        cdg_output = cdg_dask
        self.output().write_dask(cdg_output, compression="gzip")


class ETLAnalysis(Task):
    """Created an abstract class for conducting analysis of covid data
    at different levels - by country, by year, by month and by week.  This is a luigi
    task and sub-classed by the different levels of covid data analysis tasks.  The analysis
    abstract class requires Cleanup and the parquet files for performing
    the analysis and display.

    This abstract class has one analysis method to override / implement in their
    respective tasks.

    Each analysis should be a separate Luigi task, which computes its analysis and writes
    the result to parquet. To display to the terminal or answer a quiz, the output should
    be read back from the written parquet file.

    Parameters:
        subset: bool, True to process just one partition, False to process
            the entire dataset, default: True
        analysis_path: str, base directory to store output files

    Output:
        Dataframe stored in compressed Parquet format in
            {task.analysis_path}/{task.sub_dir}/subset-{task.subset}/
    """

    subset = BoolParameter(default=True)
    analysis_path = Parameter(default="./data/covid/")

    requires = Requires()
    input_data = Requirement(CovidDataGlobalCleanupTask)

    # the output references a "sub_dir" parameter, which is expected to be defined
    # in a subclass
    output = TargetOutput(
        "{task.analysis_path}{task.sub_dir}",
        ext="subset-{task.subset}/",
        target_class=ParquetTarget,
        flag="_SUCCESS",
    )

    def perform_analysis(self, df):
        """ this method will be implemented by sub-classes. """
        raise NotImplementedError

    def run(self):
        """
        Uses the data points we need for analysis -> Country_Region and Date
        calls the implemented perform_analysis method to do the calculations
        """
        analysis_dataframe = self.input()["input_data"].read_dask()

        # invoke perform_analysis from the implemented sub-classes
        # only gets the aggregated analysis column and the calculated column
        output_dataframe = self.perform_analysis(analysis_dataframe)
        # write_dask parquet file output with gzip compression.
        self.output().write_dask(output_dataframe, write_index=True, compression="gzip")


class ETLAnalysisPrint(Task):
    """
    ETL analysis class to read_dask, compute and print.  This is implemented by the
    different analysis tasks to just do that.  Last bit of work for each task to do the
    computation and print.

    Parameters:
        subset: bool, used to subset true or false, default: True
        analysis_path: str, final results are stored as parquet files here

    Output:
        print the analysis dataframe for visual
    """

    # Default parameters
    subset = BoolParameter(default=True)
    analysis_path = Parameter(default="./data/covid/")

    requires = Requires()

    def complete(self):
        """
        Does really nothing and returns false.
        """
        return False

    def run(self):
        """
        Read the dask, compute and print.
        """
        analysis_output_dataframe = self.input()["input_data"].read_dask()
        logging.info(analysis_output_dataframe.compute())


class ByCountryCovidAnalysis(ETLAnalysis):
    """
    This class extends ETLAnalysis and implements perform_analysis method.  Calculates the
    sum of confirmed cases for covid data by country and returns the dataframe.
    This class also sets the sub directory for storing the parquet file under by_country folder.
    """

    # sub directory for decade parquet file store
    sub_dir = Parameter(default="by_country/")

    def perform_analysis(self, analysis_dataframe):
        """Performs actual computation of confirmed cases by country.

        Args:
            analysis_dataframe: Covid data

        Returns:
            dataframe that contains the calculated results
        """

        analysis_dataframe["Country"] = analysis_dataframe["Country/Region"]
        analysis_dataframe["Confirmed"] = analysis_dataframe[
            (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
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


class ByCountryCovid(ETLAnalysisPrint):
    """
    this class defines the requirement - ByCountryAnalysis and does the results print.
    """

    input_data = Requirement(ByCountryCovidAnalysis)


class ByCountryMonthCovidAnalysis(ETLAnalysis):
    """
    This class extends ETLAnalysis and implements perform_analysis method.  Calculates the
    sum of confirmed cases for covid data by country, month and returns the dataframe.
    This class also sets the sub directory for storing the parquet file under by_country_month folder.
    """

    # sub directory for decade parquet file store
    sub_dir = Parameter(default="by_country_month/")

    def perform_analysis(self, analysis_dataframe):
        """Performs actual computation of confirmed cases by country and month.

        Args:
            analysis_dataframe: Covid data

        Returns:
            dataframe that contains the calculated results
        """

        est = timezone("EST")
        cur_date = datetime.datetime.now(est)
        logging.info(cur_date)
        number_of_days = (
            cur_date - datetime.datetime.strptime("1/22/20", "%m/%d/%y").astimezone(est)
        ).days
        logging.info(number_of_days)
        number_columns = list()
        for days in range(1, (number_of_days + 1)):
            number_columns.append(
                (datetime.datetime.now(est) - datetime.timedelta(days=days)).strftime(
                    "%-m/%-d/%y"
                )
            )
        logging.info(number_columns)

        for col_name in number_columns:
            analysis_dataframe["Country"] = analysis_dataframe["Country/Region"]
            analysis_dataframe["Year"] = datetime.datetime.strptime(
                col_name, "%m/%d/%y"
            ).year
            analysis_dataframe["Month"] = datetime.datetime.strptime(
                col_name, "%m/%d/%y"
            ).month
            analysis_dataframe["Confirmed"] = analysis_dataframe[col_name].astype(int)

        return (
            analysis_dataframe.groupby(["Country", "Year", "Month"])
            .Confirmed.max()
            .round()
            .astype(int)
            .to_frame()
        )


class ByCountryMonthCovid(ETLAnalysisPrint):
    """
    this class defines the requirement - ByCountryMonthAnalysis and does the results print.
    """

    input_data = Requirement(ByCountryMonthCovidAnalysis)
