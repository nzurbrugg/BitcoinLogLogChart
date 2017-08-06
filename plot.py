import csv
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from math import log10
import urllib

import hashlib
import hmac
import requests
import time

secret_key = input('Enter your secret key: ')
public_key = input('Enter your public key: ')

timestamp = int(time.time())
payload = '{}.{}'.format(timestamp, public_key)
hex_hash = hmac.new(secret_key.encode(), msg=payload.encode(), digestmod=hashlib.sha256).hexdigest()
signature = '{}.{}'.format(payload, hex_hash)

url = 'https://apiv2.bitcoinaverage.com/indices/global/history/BTCUSD?period=alltime&?format=csv'
headers = {'X-Signature': signature}
result = requests.get(url=url, headers=headers)

data = pandas.read_json(result.text)
date = data.time.tolist()
average = data.average.tolist()
low = data.low.tolist()
high = data.high.tolist()

genesisdate = '1/3/2009'
daysFromGenesis = mdates.datestr2num(date) - mdates.datestr2num(genesisdate)

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

datemin = datestr2x('6/1/2010')
datemax = datestr2x('1/1/2024')

def plotLineFrom2Points(date1, price1, date2, price2):
    x1=datestr2x(date1)
    x2=datestr2x(date2)
    y1=price1
    y2=price2
    
    y0=y1*(datemin/x1)**(log10(y2/y1)/log10(x2/x1))
    y3=y1*(datemax/x1)**(log10(y2/y1)/log10(x2/x1))
    
    line = plt.plot([datemin, datemax], [y0, y3], color='k', linestyle=':', label='Trend line')

    return line

years = mdates.YearLocator()
months = mdates.MonthLocator()

ax = plt.subplot(1,1,1)
#ax.loglog(daysFromGenesis, low, linewidth=1, color='0.5')
#ax.loglog(daysFromGenesis, high, linewidth=1, color='0.5')
averagePlot = ax.loglog(daysFromGenesis, average, linewidth=1, label='Daily Average Price')

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(FuncFormatter(xMajorFormat))
ax.xaxis.set_minor_locator(months)
ax.set_xlim(datemin, datemax)

ax.set_ylabel('$/BTC')
ax.yaxis.set_major_formatter(FuncFormatter(yLogFormat))
ymin = 0.01
ymax = 40000
ax.set_ylim(ymin, ymax)

ax.grid(b=True, which='major', color='0.8', linestyle='-')
ax.grid(b=True, which='minor', color='0.96', linestyle='-')
ax.set_axisbelow(True)

#halving dates
plt.axvline(x=datestr2x('11/28/2012'), color='r', linestyle="--", label='Mining reward halving dates')
plt.axvline(x=datestr2x('7/10/2016'), color='r', linestyle="--")
plt.axvline(x=datestr2x('3/10/2020'), color='r', linestyle="--")
plt.axvline(x=datestr2x('12/10/2023'), color='r', linestyle="--")

#low boundary line
plotLineFrom2Points('12/10/2010',0.19,'5/23/2016',443.77)
#plotLineFrom2Points('12/10/2010',0.22,'9/15/2015',228)

#low average line
#plotLineFrom2Points('12/10/2010',0.3,'5/23/2016',570)

#low peak line
#plt.plot([1.5*365, 15*365], [0.2, 50000], color='k', linestyle=':')
#plotLineFrom2Points('11/7/2010',0.36,'11/4/2015',490)

#high peak line
#plt.plot([datestr2x('6/9/2011'), datestr2x('11/29/2013'), datestr2x('4/1/2018'), 15*365], [29.58, 600, 10000, 90000], color='k', linestyle=':')

plt.legend(loc='upper left')

plt.show()

