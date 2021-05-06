
import datetime
from pytz import timezone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler


def covid_data_ml_predict():
    est = timezone('EST')
    cur_date = datetime.datetime.now(est)
    print(cur_date)
    number_of_days = (cur_date - datetime.datetime.strptime("1/22/20", '%m/%d/%y').astimezone(est)).days
    print(number_of_days)
    number_columns = list()
    for days in range(1, (number_of_days + 1)):
        number_columns.append((datetime.datetime.now(est) - datetime.timedelta(days=days)).strftime("%#m/%#d/%y"))
    df = pd.read_parquet('../../data/covid/subset-False/part.0.parquet', engine='pyarrow')
    idx = ['Province/State', 'Country/Region', 'Lat', 'Long']
    melt_df = pd.melt(df,
                      id_vars=idx,
                      value_vars=number_columns,
                      var_name='Date').sort_values(idx).reset_index(drop=True)
    print(melt_df)

    melt_df.drop(columns=['Province/State', 'Lat', 'Long'], inplace=True)
    melt_df.info()
    melt_df['Date'] = pd.to_datetime(melt_df['Date'])
    melt_df.info()
    melt_df.sort_values(['Country/Region', 'Date'])
    new_df = melt_df.groupby(['Country/Region', 'Date']).sum()
    print(melt_df.groupby(['Country/Region', 'Date']).sum())
    print(new_df)
    print(new_df.to_string(index=True, max_rows=50))
    print(new_df.diff())
    new2_df = new_df.diff()
    print(new2_df)
    print(new2_df.to_string(index=True, max_rows=100))

    last_seven_days_date = datetime.datetime.now() - datetime.timedelta(days=7)
    print(last_seven_days_date)
    new3_df = new2_df[new2_df.index.get_level_values('Date') >= last_seven_days_date]
    print(new3_df)
    print(new3_df.to_string(index=True, max_rows=100))

    print(new3_df[new3_df.index.isin(['India'], level=0)])


if __name__ == "__main__":
    covid_data_ml_predict()
