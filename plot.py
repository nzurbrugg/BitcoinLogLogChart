import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from math import log10
from scipy import optimize
import datetime as dt
from datetime import timedelta


# --- Collect data
# https://www.investing.com/crypto/bitcoin/historical-data
price = pandas.read_csv('Bitcoin Historical Data.csv', thousands=',', index_col='Date')
price.index = pandas.to_datetime(price.index, format='%m/%d/%Y').date
print(price)

# https://data.nasdaq.com/data/FED/M2_N_WM-m2-not-seasonally-adjusted-weekly-monday
M2 = pandas.read_csv('FED-M2_N_WM.csv', index_col='Date')
M2.index = pandas.to_datetime(M2.index, format='%Y-%m-%d').date
M2['Value'] = M2['Value'] * 1E9
M2.rename(columns={'Value':'M2'}, inplace = True)
print(M2)

# https://data.nasdaq.com/data/BCHAIN/TOTBC-total-bitcoins
BTC = pandas.read_csv('BCHAIN-TOTBC.csv', index_col='Date')
BTC.index = pandas.to_datetime(BTC.index, format='%Y-%m-%d').date
BTC.rename(columns={'Value':'total-bitcoins'}, inplace = True)

# Merge data
price_BTC = price.merge(BTC, left_index=True, right_index=True, how='left')
df = price_BTC.merge(M2, left_index=True, right_index=True, how='left')
df = df.interpolate().ffill().bfill()
#df = df.drop(pandas.to_datetime('2010-07-18')) # this row was causing errors for some reason, so removed it

# Extend a separate dataframe for extending fitted curves
edf = pandas.DataFrame(index=pandas.date_range(start='2010-07-19', end='2028-01-01', freq='D'))

genesisdate = pandas.Timestamp('1/3/2009') #'10/5/2009'
df['days_since'] = (pandas.to_datetime(df.index) - genesisdate).days
M2['days_since'] = (pandas.to_datetime(M2.index) - genesisdate).days
edf['days_since'] = (pandas.to_datetime(edf.index) - genesisdate).days

# --- Curve fitting ---
def ffa(df, a, b, c, d):
    days_since = df['days_since']
    return a * np.log(days_since - b) + c

def ffb(df, a, b, c, d):
    days_since = df['days_since']
    BTC_supply = df['total-bitcoins']
    M2_supply = df['M2']
    return  (a * np.log(days_since - b) + c) * np.log(M2_supply / BTC_supply)

def devfit(df, a, b, c, d):
    days_since = df['days_since']
    return a * np.exp(d * (days_since - b)) + c

def lowdevfit(df, a, b, c, d):
    days_since = df['days_since']
    return a

#df = df[(df.index <= dt.date(2020,5,7))]

x0 = [5, 0, -30, 1]
parama, pcova = optimize.curve_fit(ffa, xdata=df, ydata=np.log(df['Price']), p0=x0)
print(parama)
df['fita'] = np.exp(ffa(df, *parama))
edf['fita'] = np.exp(ffa(edf, *parama))
df['deviation'] = (df['Price'] - df['fita']) / df['fita']

edf['lowfita'] = edf['fita'] * 0.4

low11 = dt.date(2010,10,25)
low12 = dt.date(2010,12,25)
low13 = dt.date(2011,1,29)
low14 = dt.date(2011,4,9)
low21 = dt.date(2011,11,18)
low22 = dt.date(2012,2,18)
low23 = dt.date(2012,5,10)
low24 = dt.date(2012,10,26)
low25 = dt.date(2013,1,2)
low31 = dt.date(2015,8,24)
low32 = dt.date(2016,2,3)
low33 = dt.date(2016,5,22)
low34 = dt.date(2016,8,2)
low35 = dt.date(2017,1,11)
low36 = dt.date(2017,3,25)
low41 = dt.date(2018,12,14)
low42 = dt.date(2019,2,6)
low43 = dt.date(2020,3,12)
low44 = dt.date(2020,9,22)
low51 = dt.date(2022,11,21)

lowspread = timedelta(days=0)
lowdf  = df[((df.index >= low11 - lowspread) & (df.index <= low11 + lowspread))
          #| ((df.index >= low12 - lowspread) & (df.index <= low12 + lowspread))
          #| ((df.index >= low13 - lowspread) & (df.index <= low13 + lowspread))
          #| ((df.index >= low14 - lowspread) & (df.index <= low14 + lowspread))
          #| ((df.index >= low21 - lowspread) & (df.index <= low21 + lowspread))
          #| ((df.index >= low22 - lowspread) & (df.index <= low22 + lowspread))
          #| ((df.index >= low23 - lowspread) & (df.index <= low23 + lowspread))
          #| ((df.index >= low24 - lowspread) & (df.index <= low24 + lowspread))
          | ((df.index >= low25 - lowspread) & (df.index <= low25 + lowspread))
          | ((df.index >= low31 - lowspread) & (df.index <= low31 + lowspread))
          #| ((df.index >= low32 - lowspread) & (df.index <= low32 + lowspread))
          #| ((df.index >= low33 - lowspread) & (df.index <= low33 + lowspread))
          #| ((df.index >= low34 - lowspread) & (df.index <= low34 + lowspread))
          #| ((df.index >= low35 - lowspread) & (df.index <= low35 + lowspread))
          #| ((df.index >= low36 - lowspread) & (df.index <= low36 + lowspread))
          #| ((df.index >= low41 - lowspread) & (df.index <= low41 + lowspread))
          #| ((df.index >= low42 - lowspread) & (df.index <= low42 + lowspread))
          | ((df.index >= low43 - lowspread) & (df.index <= low43 + lowspread))
          #| ((df.index >= low44 - lowspread) & (df.index <= low44 + lowspread))
          | ((df.index >= low51 - lowspread) & (df.index <= low51 + lowspread))]

#lowdf = df[((df.index >= dt.date(2010, 7,19)) & (df.index <= dt.date(2011, 4, 5)))
#         | ((df.index >= dt.date(2011,10,29)) & (df.index <= dt.date(2013, 1,28)))
#         | ((df.index >= dt.date(2015, 8,16)) & (df.index <= dt.date(2017, 3,26)))
#         | ((df.index >= dt.date(2018,12,15)) & (df.index <= dt.date(2019, 4, 1)))
#         | ((df.index >= dt.date(2019,11,22)) & (df.index <= dt.date(2020,10,17)))]

peak1 = dt.date(2011,6,8)
peak2 = dt.date(2013,12,4)
peak3 = dt.date(2017,12,16)
peak4 = dt.date(2021,4,13)
peakspread = timedelta(days=0)

highdf = df[((df.index >= peak1 - peakspread) & (df.index <= peak1 + peakspread))
          | ((df.index >= peak2 - peakspread) & (df.index <= peak2 + peakspread))
          | ((df.index >= peak3 - peakspread) & (df.index <= peak3 + peakspread))
          | ((df.index >= peak4 - peakspread) & (df.index <= peak4 + peakspread))]

parama, pcova = optimize.curve_fit(devfit, xdata=highdf, ydata=highdf['deviation'], p0=[17,500,0.6,-0.0001])
df['highdevfit'] = devfit(df, *parama)
edf['highdevfit'] = devfit(edf, *parama)
edf['highfit'] = edf['highdevfit'] * edf['fita'] + edf['fita']
print(parama)

parama, pcova = optimize.curve_fit(lowdevfit, xdata=lowdf, ydata=lowdf['deviation'], p0=[-0.6,0,0,0])
df['lowdevfit'] = lowdevfit(df, *parama)
edf['lowdevfit'] = lowdevfit(edf, *parama)
edf['lowfit'] = edf['lowdevfit'] * edf['fita'] + edf['fita']
print(parama)

df['bestdevfit'] = 0
edf['bestdevfit'] = 0

parama, pcova = optimize.curve_fit(ffa, xdata=highdf, ydata=np.log(highdf['Price']), p0=x0)
edf['highfita'] = np.exp(ffa(edf, *parama))

# --- Plot ---
#plot = 'M2'
#plot = 'BTC'
#plot = 'M2/BTC'
plot = 'Price'

if plot == 'M2':
    ax = plt.subplot(1,1,1)
    ax.semilogy(M2.index, M2['M2'])
    #ax.plot(M2.index, M2['M2fit'])
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.set_ylim([0,None])

if plot == 'BTC':
    ax = plt.subplot(1,1,1)
    ax.plot(BTC.index, BTC['total-bitcoins'])
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.set_ylim([0,None])

if plot == 'M2/BTC':
    ax = plt.subplot(1,1,1)
    ax.plot(df.index, df['Value'] / df['total-bitcoins'])
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.set_ylim([0,None])

if plot == 'Price':
    fig, (a1, a2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios':[3,1]})
    plt.tight_layout()
    a1.semilogy(df.index, df['Price'], linewidth=1, label='Daily Average', color='blue')
    a1.semilogy(edf.index, edf['fita'], linewidth=1, label='Total Best Fit Curve', color='orange')
    a1.semilogy(edf.index, edf['highfit'], linewidth=1, label='High best fit curve', color='red')
    a1.semilogy(edf.index, edf['lowfit'], linewidth=1, label='Low best fit curve', color='green')
    a1.scatter(lowdf.index, lowdf['Price'])
    a1.set(ylabel='USD Price\n(log scale)')
    a1.set_ylim([0.01,1E7])
    
    #halving dates
    a1.axvline(x=dt.date(2009,1,3), color='gray', linestyle="--", label='Mining reward halving dates')
    a1.axvline(x=dt.date(2012,11,28), color='gray', linestyle="--")
    a1.axvline(x=dt.date(2016,7,9), color='gray', linestyle="--")
    a1.axvline(x=dt.date(2020,5,12), color='gray', linestyle="--")
    a1.axvline(x=dt.date(2024,4,1), color='gray', linestyle="--")
    a1.axvline(x=dt.date(2028,1,11), color='gray', linestyle="--")
    a1.axvline(x=dt.date(2031,11,11), color='gray', linestyle="--")
    
    a1.legend(loc='upper left')

    a2.plot(df.index, df['deviation'], color='blue')
    a2.plot(df.index, df['bestdevfit'], color='orange')
    a2.plot(df.index, df['lowdevfit'], color='green')
    a2.plot(df.index, df['highdevfit'], color='red')
    a2.scatter(lowdf.index, lowdf['deviation'])
    a2.set(ylabel='% deviation\n from Total Best Fit Curve')
    
    a1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    a2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

	
plt.show()
