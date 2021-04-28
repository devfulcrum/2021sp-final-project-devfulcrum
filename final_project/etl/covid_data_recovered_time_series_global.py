import luigi
import requests
from luigi import Parameter


class CovidDataRecoveredTimeSeriesGlobal(luigi.Task):

    etl_url = Parameter()

    def output(self):
        return luigi.LocalTarget("data/time_series_covid19_recovered_global.csv")

    def run(self):
        with self.output().open("w") as f:
            r = requests.get(self.etl_url, allow_redirects=True)
            f.write(r.content.decode("utf-8"))


if __name__ == "__main__":
    luigi.run(["CovidDataRecoveredTimeSeriesGlobal", "--local-scheduler"])
