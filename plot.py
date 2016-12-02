import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from math import log10
import urllib

urllib.urlretrieve("https://api.bitcoinaverage.com/history/USD/per_day_all_time_history.csv", 'per_day_all_time_history.csv')
data = pandas.read_csv('per_day_all_time_history.csv')
date = data.DateTime.tolist()
average = data.Average.tolist()
low = data.Low.tolist()
high = data.High.tolist()

genesisdate = '1/3/2009'
daysFromGenesis = mdates.datestr2num(date) - mdates.datestr2num(genesisdate)

fig, ax = plt.subplots()
#ax.loglog(daysFromGenesis, low, linewidth=1, color='0.5')
#ax.loglog(daysFromGenesis, high, linewidth=1, color='0.5')
averagePlot = ax.loglog(daysFromGenesis, average, linewidth=1, label='Daily Average Price')

ax.set_ylabel('$/BTC')

years = mdates.YearLocator()
months = mdates.MonthLocator()

def datestr2x(datestr):
    x = mdates.datestr2num(datestr) - mdates.datestr2num(genesisdate)
    return x
    
def xMajorFormat(x,pos=None):
    date = mdates.num2date(x + mdates.datestr2num(genesisdate))
    label = date.strftime('%Y')
    return label

def yLogFormat(y,pos):
    decimalplaces= int(np.maximum(-np.log10(y),0))
    formatstring = '{{:.{:1d}f}}'.format(decimalplaces)
    return formatstring.format(y)

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(FuncFormatter(xMajorFormat))
ax.xaxis.set_minor_locator(months)

datemin = datestr2x('6/1/2010')
datemax = datestr2x('1/1/2024')
ax.set_xlim(datemin, datemax)

ax.yaxis.set_major_formatter(FuncFormatter(yLogFormat))
ymin = 0.01
ymax = 40000
ax.set_ylim(ymin, ymax)

def plotLineFrom2Points(date1, price1, date2, price2):
    x1=datestr2x(date1)
    x2=datestr2x(date2)
    y1=price1
    y2=price2
    
    y0=y1*(datemin/x1)**(log10(y2/y1)/log10(x2/x1))
    y3=y1*(datemax/x1)**(log10(y2/y1)/log10(x2/x1))
    
    line = plt.plot([datemin, datemax], [y0, y3], color='k', linestyle=':', label='Trend line')

    return line

ax.grid(b=True, which='major', color='0.8', linestyle='-')
ax.grid(b=True, which='minor', color='0.96', linestyle='-')
ax.set_axisbelow(True)

#halving dates
plt.axvline(x=datestr2x('11/28/2012'), color='r', linestyle="--", label='Mining reward halving dates')
plt.axvline(x=datestr2x('7/10/2016'), color='r', linestyle="--")
plt.axvline(x=datestr2x('3/10/2020'), color='r', linestyle="--")
plt.axvline(x=datestr2x('12/10/2023'), color='r', linestyle="--")
###peak dates

#new high peaks
#plt.axvline(x=datestr2x('11/7/2010'), linestyle="--")
#plt.axvline(x=datestr2x('2/13/2011'), linestyle="--")
#plt.axvline(x=datestr2x('6/9/2011'), linestyle="--")
#plt.axvline(x=datestr2x('4/9/2013'), linestyle="--")
#plt.axvline(x=datestr2x('11/29/2013'), linestyle="--")

#rebound peaks
#plt.axvline(x=datestr2x('1/8/2012'), linestyle="--")
#plt.axvline(x=datestr2x('8/17/2012'), linestyle="--")

#weak rebound peaks
#plt.axvline(x=datestr2x('7/1/2014'), linestyle="--", color='0.8')
#plt.axvline(x=datestr2x('11/14/2014'), linestyle="--", color='0.8')
#plt.axvline(x=datestr2x('11/4/2015'), linestyle="--", color='0.8')

#predicted peaks
#plt.axvline(x=datestr2x('2/1/2017'), linestyle="--", color='0.8')
#plt.axvline(x=datestr2x('4/1/2018'), linestyle="--", color='0.8')

#low boundary line
plotLineFrom2Points('12/10/2010',0.19,'5/23/2016',443.77)

#low peak line
#plt.plot([1.5*365, 15*365], [0.2, 50000], color='k', linestyle=':')
#plotLineFrom2Points('11/7/2010',0.36,'11/4/2015',490)

#high peak line
#plt.plot([datestr2x('6/9/2011'), datestr2x('11/29/2013'), datestr2x('4/1/2018'), 15*365], [29.58, 600, 10000, 90000], color='k', linestyle=':')

plt.legend(loc='upper left')

plt.show()

