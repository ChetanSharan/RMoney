#Step One: Fetch Stock Data
import yfinance as yf
aapl = yf.Ticker("AAPL")
hist = aapl.history(period='2y',interval= "1h")

#Step Two: Calculate Rolling Maximum and Minimum
hist['max_price']= hist['Close'].rolling(window=20).max()
hist['min_price']= hist['Close'].rolling(window=20).min()

#Step Three: Determine Trading Signals
hist['Short_signal']= hist['Close']>=hist['max_price']
hist['Long_signal']= hist['Close']<=hist['min_price']

#Step Four: Signal Processing
hist.loc[hist['Long_signal']==True,'Signal']=1
hist.loc[hist['Short_signal']==True,'Signal']=-1

#Step Five: Calculate Positions
hist['Position0']=hist['Signal'].ffill()
hist['Position1'] = hist['Position0'].diff()
import numpy as np
hist['Position1']= np.where(hist['Position1']!=0.0,hist['Signal'],0)
hist['Position2']=hist['Position1']*hist['Close']

#Step Six: Filtering and Return Calculation
df_ret=hist[hist['Position1']!=0].copy()
df_ret.dropna(subset=['Position2'],inplace=True)
df_ret['abs_returns'] =  df_ret['Position2'].rolling(2).sum()
df_ret.loc[::2,'abs_returns'] = '0'
df_ret['abs_returns']=df_ret['abs_returns'].astype(float)
df_ret['Position2_shifted'] = df_ret['Position2'].shift(1)
df_ret['pct_returns'] = (df_ret['abs_returns'] / df_ret['Position2_shifted'])*100
df_ret['pct_returns'] = df_ret['pct_returns'].fillna(0)
df_ret = df_ret.drop(columns=['Position2_shifted'])
df_ret['pct_returns_cumsum']=df_ret['pct_returns'].cumsum()

#Step Seven: Save the Results
df_ret.to_csv('aaa_returns.csv')