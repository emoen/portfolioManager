import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as math

import sys
import os


startMoney = np.float64(sys.argv[1])
print type(startMoney)
#print "startMoney",startMoney
ordersCsv = sys.argv[2]
#print "orderCsv", ordersCsv
valuesCsv = sys.argv[3]
#print "valuesCsv", valuesCsv

trades = pd.read_csv(ordersCsv, sep=',', header=None)

#print trades

symbols = set()
dates = []

rows, cols = trades.shape
#print "rows:",rows
#print "cols",cols
for x in range(0, rows ):
    symbols.add(trades.iloc[x,3])
    aDate = dt.datetime(trades.iloc[x,0], trades.iloc[x,1], trades.iloc[x,2])
    #print "aDate", aDate
    dates.append(aDate)

#print "dates", dates
sortedDates = dates.sort()

#print symbols
#print "daterange:",dates[0]," to:", dates[rows-1]

dt_timeofday = dt.timedelta(hours=16)
ls_keys = ['close']
#print "last date:",dates[rows-1] + dt.timedelta(days=1)
ldt_timestamps = du.getNYSEdays(dates[0], dates[rows-1] + dt.timedelta(days=1), dt_timeofday)

c_dataobj = da.DataAccess('Yahoo')

#ls_symbols = c_dataobj.get_symbols_from_list('sp5002012')
#symbolsFile = "symbols.txt"
#os.path.exists(symbolsFile) and os.remove(symbolsFile)
#f = open(symbolsFile,'a+')
#for item in ls_symbols:
#    f.write("%s\n" % item)

ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
dataFrame_price = ldf_data[0]

#list(ldf_data.columns.values)
#print ldf_data[0].values
#print len(ldf_data)
#print ldf_data[0].columns.values.tolist()
#print ldf_data[0].index.tolist()
#print type(trades)
#print trades.columns.values
#print ldf_data[0].index.tolist()


#print "index type:",type(ldt_timestamps[0])
#print "trading days:",ldt_timestamps
#print dataFrame_price.index
#print type(dataFrame_price.index)
#print len(dataFrame_price.index)

trades1 = trades.sort([0,1,2])
tradingDays = len(dataFrame_price.index)
cash = [startMoney] * tradingDays
initOwnStocks = dict.fromkeys(list(symbols), np.zeros(tradingDays))
own = pd.DataFrame(initOwnStocks, index=ldt_timestamps)
equityValue = [0] * tradingDays
#print np.zeros(tradingDays)
#print "own",own
#print "own index",own.columns.values.tolist()


#someDate = dt.datetime(trades1.iloc[4,0],trades1.iloc[4,1],trades1.iloc[4,2],16, 0,0)
#print dataFrame_price.index.get_loc(someDate)

for x in range(0, rows ):
    theDate = dt.datetime(trades1.iloc[x,0],trades1.iloc[x,1],trades1.iloc[x,2],16, 0,0)
    pdTime = pd.Timestamp(theDate)
    strTime = pdTime.strftime('%Y-%m-%d %H:00:00')
    theSymbol = trades1.iloc[x,3]
    numberOfShares = trades1.iloc[x,5]
    
    if trades1.iloc[x,4] == 'Buy':
        #theDate = '',trades1.iloc[x,0],'-',trades1.iloc[x,1],'-',trades1.iloc[x,2],' 16:00:00' #, dt_timeofday
        #print "theDate",theDate
        #print type(theDate)  
        #print "timestamp", pdTime
        #print "type:",type(pdTime)  
        #print "strTime:",strTime
        #print dataFrame_price.ix[strTime, theSymbol]

        cost = dataFrame_price.ix[strTime, theSymbol] * numberOfShares
        cashDateToArrayIndex = dataFrame_price.index.get_loc(strTime)
        cash[cashDateToArrayIndex] = cash[cashDateToArrayIndex] - cost
        accumulatedShares = own.ix[strTime, theSymbol] + numberOfShares   
        own.ix[strTime,theSymbol] = accumulatedShares
        for rest in range(cashDateToArrayIndex,tradingDays):
            cash[rest] = cash[cashDateToArrayIndex]
            nextDate = ldt_timestamps[rest]
            own.ix[nextDate,theSymbol] = accumulatedShares
        
    if trades1.iloc[x,4] == 'Sell':
        income = dataFrame_price.ix[strTime, theSymbol] * trades1.iloc[x,5]
        cashDateToArrayIndex = dataFrame_price.index.get_loc(strTime)
        cash[cashDateToArrayIndex] = cash[cashDateToArrayIndex] + income
        reducedShares = own.ix[strTime, theSymbol] - numberOfShares   
        own.ix[strTime,theSymbol] = reducedShares
        for rest in range(cashDateToArrayIndex,tradingDays):
            cash[rest] = cash[cashDateToArrayIndex]
            nextDate = ldt_timestamps[rest]
            own.ix[nextDate,theSymbol] = reducedShares

#print "cash",cash
#print "own",own.ix[:,'AAPL']

i = 0
for currDate in ldt_timestamps:
    todaysValue = 0
    for aSymb in symbols:
        todaysValue = todaysValue + (dataFrame_price.ix[currDate, aSymb] * own.ix[currDate,aSymb])
    equityValue[i] = todaysValue
    i = i+1

#print "equityValue",equityValue

os.path.exists(valuesCsv) and os.remove(valuesCsv)
f = open(valuesCsv,'a+')

total = [0] * tradingDays
for j in range(0, tradingDays):
    total[j] = equityValue[j] + cash[j]
    
    valueAtTime = ldt_timestamps[j].strftime('%Y,%m,%d')
    f.write(valueAtTime + ",%.2f\n" % total[j]) 
    
#print "total",total

daily_return = []
for xx in range(0, tradingDays ):
    if xx > 0:
        daily_return.append( total[xx] / total[xx-1] )
    else: daily_return.append( total[xx] / total[xx] )   

total_return = total[tradingDays-1]  / total[0]
#avg_daily =  (total_return - 1)/ tradingDays #!ok - wrong
avg_daily = np.mean(tsu.returnize0(total))
std_return = np.std(daily_return, axis=0) #ok
sharp = (avg_daily/std_return) * (np.sqrt(tradingDays)) #!ok

print "sharp",sharp
print "total_return",total_return
print "stddev", std_return
print "daily return", avg_daily
print "trading days", tradingDays

#print "6 desember",dataFrame_price.index.get_loc("2011-12-6 16:00:00") #-> 229 - egentlig 230
#print "tdays",tradingDays
#print ldt_timestamps

#print "size total",len(total)
#print total[230]

#print "9 nov",dataFrame_price.index.get_loc("2011-11-9 16:00:00") #-> 211 - egentlig 212?
#print total[211]

#print "26 sept",dataFrame_price.index.get_loc("2011-09-26 16:00:00") #-> 179 - egentlig 179
#print total[179]

#print "21 juli",dataFrame_price.index.get_loc("2011-07-21 16:00:00") #-> 133 - egentlig 133
#print total[133]

##print "6 des",dataFrame_price.index.get_loc("2011-12-06 16:00:00") #-> 225  orders2
#print total[225]

#print "9 nov",dataFrame_price.index.get_loc("2011-11-09 16:00:00") #-> 207  orders2
#print total[207]

#print "26 sept",dataFrame_price.index.get_loc("2011-09-26 16:00:00") #-> 175  orders2
#print total[175]

#print "21 july",dataFrame_price.index.get_loc("2011-07-21 16:00:00") #-> 175  orders2
#print total[129]
        
#print "28 march",dataFrame_price.index.get_loc("2011-03-28 16:00:00") #-> 175  orders2
#print total[49]
        