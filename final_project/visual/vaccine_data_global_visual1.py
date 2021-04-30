import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datashader as ds
from datashader import transfer_functions as tf


def read_vaccine_data_file():
    sns.set_theme(style="whitegrid")
    df = pd.read_csv("../../data/vaccine_data_global.csv")
    df_filter = df["Doses_admin"] > 199999999
    print(df[df_filter])
    df_doses_admin_over_200mil = df[df_filter]
    df_doses_admin_over_200mil = df_doses_admin_over_200mil[["Country_Region", "Doses_admin",
                                                             "People_fully_vaccinated"]]
    print(df_doses_admin_over_200mil)
    sns.barplot(x="Country_Region", y="Doses_admin", hue="People_fully_vaccinated", data=df_doses_admin_over_200mil)

    # lat, lon for every person in census!
    # cvs = ds.Canvas(plot_width=850, plot_height=500)
    # agg = cvs.points(df,
    #                  'lon'
    #                  ,
    #                  'lat')
    # tf.shade(agg, how='eq_hist')

    plt.show()
    return


# colorbrewer2.org
# dash.plotly.com
# holoviz.org
# bokeh
# matplotlib
# seaborn
if __name__ == "__main__":
    read_vaccine_data_file()
