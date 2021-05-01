import luigi
import requests
from luigi import Parameter


class VaccineDataGlobal(luigi.Task):
    """
    This luigi task class is to work with Vaccine data time series
    information download for Global
    """

    etl_url = Parameter()

    def output(self):
        """
        This function returns the Local target for data download.

        :return:
            LocalTarget: returns luigi.LocalTarget for vaccine_data_global.csv
        """

        return luigi.LocalTarget("data/vaccine_data_global.csv")

    def run(self):
        """
        This function uses the etl_url parameters to perform http get request and
        write the response content to the local target.

        :return:
            File content is stored in the data directory
        """

        with self.output().open("w") as f:
            r = requests.get(self.etl_url, allow_redirects=True)
            f.write(r.content.decode("utf-8"))


if __name__ == "__main__":
    """
    This is to just to test the code locally.
    """
    luigi.run(["VaccineDataGlobal", "--local-scheduler"])
