import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import os
import matplotlib.pyplot as plt
import operator


def plot(df_close, ldt_timestamps, ls_symbols, data_mean, mean_pluss_std, mean_minus_std, bollinger_val):
    na_price = df_close.values
    plt.clf()
    
    fig = plt.figure()
    fig.add_subplot(211)
    plt.plot(ldt_timestamps, na_price)
    plt.plot(ldt_timestamps, data_mean)
    plt.plot(ldt_timestamps, mean_pluss_std)
    plt.plot(ldt_timestamps, mean_minus_std)

    meanMinus =  [val for sublist in mean_minus_std.values for val in sublist]
    meanPlus = [val for sublist in mean_pluss_std.values for val in sublist]

    plt.fill_between(ldt_timestamps, meanMinus, meanPlus, color='gray',alpha=0.2)
    plt.ylabel('actual_close') #Adjusted Close
    plt.xlabel('Date')
    
    fig.add_subplot(212)
    plt.plot(ldt_timestamps, bollinger_val)
    ones = np.array([1] * len(bollinger_val))
    
    plt.plot(ldt_timestamps, ones, color='gray')    
    plt.plot(ldt_timestamps, ones * -1, color='gray') 
    plt.fill_between(ldt_timestamps, ones*-1, 1, color='gray',alpha=0.2)

    print bollinger_val.values[18]
    flag_buy = False
    flag_sold = False
    for i in range(LOOKBACK-1, len(bollinger_val.values)):
        if bollinger_val.values[i] >= 1 and flag_sold == False:
            plt.axvline(x=ldt_timestamps[i], color='red', lw=1, alpha=0.5)
            flag_sold = True
            flag_buy = False
        if bollinger_val.values[i] <= -1 and flag_buy == False:
            plt.axvline(x=ldt_timestamps[i], color='green', lw=1, alpha=0.5)
            flag_sold = False
            flag_buy = True
    plt.savefig('boolinger.pdf', format='pdf')    

LOOKBACK = 20
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
ls_symbols = ["MSFT"]
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

dataobj = da.DataAccess('Yahoo')
ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)

d_data = dict(zip(ls_keys, ldf_data))

for s_key in ls_keys:
    d_data[s_key] = d_data[s_key].fillna(method='ffill')
    d_data[s_key] = d_data[s_key].fillna(method='bfill')
    d_data[s_key] = d_data[s_key].fillna(1.0)

df_close = d_data['close']

data_mean = pd.rolling_mean(df_close, window=LOOKBACK, min_periods=LOOKBACK)
data_std = pd.rolling_std(df_close, window=LOOKBACK, min_periods=LOOKBACK)
mean_pluss_std = data_mean + data_std
mean_minus_std = data_mean - data_std
bollinger_val = (df_close.values - data_mean) / (data_std)
#print ldt_timestamps[89]
#print ldt_timestamps[96]
#print ldt_timestamps[111]
#print ldt_timestamps[118]

    
df_events = copy.deepcopy(df_close)

plot(df_close, ldt_timestamps, ls_symbols, data_mean, mean_pluss_std, mean_minus_std, bollinger_val)


