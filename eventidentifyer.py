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

print "Creating Study"

dt_start = dt.datetime(2008, 1, 1)
dt_end = dt.datetime(2009, 12, 31)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

dataobj = da.DataAccess('Yahoo')
ls_symbols = dataobj.get_symbols_from_list('sp5002012')
ls_symbols.append('SPY')

ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))

for s_key in ls_keys:
    d_data[s_key] = d_data[s_key].fillna(method='ffill')
    d_data[s_key] = d_data[s_key].fillna(method='bfill')
    d_data[s_key] = d_data[s_key].fillna(1.0)

df_close = d_data['actual_close']

print "Creating Study"

df_events = copy.deepcopy(df_close)
df_events = df_events * np.NAN

print "Creating Study"

# Time stamps for the event range
ldt_timestamps = df_close.index

myOrdersCsv = 'myorders.csv'
os.path.exists(myOrdersCsv) and os.remove(myOrdersCsv)
f = open(myOrdersCsv,'a+')
count=0
for s_sym in ls_symbols:
    for i in range(1, len(ldt_timestamps)):
        # Calculating the returns for this timestamp
        f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
        f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
        f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1

        if f_symprice_yest >=10.0 and f_symprice_today < 10.0:
            count +=1
            df_events[s_sym].ix[ldt_timestamps[i]] = 1
            buyTime = ldt_timestamps[i].strftime('%Y,%m,%d')
            f.write(buyTime + "," + s_sym + ",Buy,100\n") 
            if i+5 < len(ldt_timestamps):
                strSellTime = ldt_timestamps[i+5].strftime('%Y,%m,%d')
                f.write(strSellTime + "," + s_sym + ",Sell,100\n") 
            else: 
                strSellTime = ldt_timestamps[-1].strftime('%Y,%m,%d')
                f.write(strSellTime + "," + s_sym + ",Sell,100\n")                

print "Creating Studies found:", count
#ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
#            s_filename='week6-1-2012-5_actualClose.pdf', b_market_neutral=True, b_errorbars=True,
#            s_market_sym='SPY')

