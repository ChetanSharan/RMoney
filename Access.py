import yfinance as yf
import numpy as np

# Parameters
ticker = 'AAPL'
lookback = 20

"""
Step One: Fetch Stock Data
"""
df_hist = yf.Ticker(ticker).history(period = '2y',interval = "1h")

"""
Step Two: Calculate Rolling Maximum and Minimum
"""
df_hist['max_price'] = df_hist['Close'].rolling(window = lookback).max()
df_hist['min_price'] = df_hist['Close'].rolling(window = lookback).min()

"""
Step Three: Determine Trading Signals
"""

# It was mentioned in the problem statement that when local max/min 'matches' the ‘Close’ value, the Short/Long signal should be generated.
# However, wihh some knowledge of Finance & market behaviour, I have taken '<=' or '>=' for ‘matches’ rather than ‘=‘.
# But if it needs to be ‘equals’, then just the sign needs to be changed.

df_hist['Short_signal'] = df_hist['Close'] >= df_hist['max_price'] 
df_hist['Long_signal'] = df_hist['Close'] <= df_hist['min_price']

"""
Step Four: Signal Processing
"""
df_hist['Signal'] = np.nan
df_hist.loc[df_hist['Long_signal'] == True,'Signal'] = 1
df_hist.loc[df_hist['Short_signal'] == True,'Signal'] = -1

"""
Step Five: Calculate Positions
"""
df_hist['Position0'] = df_hist['Signal'].ffill()

# Here, its requested that I need to identify positions' initiation for Position1.
# So, I have taken +1 & -1 that represets the positions' initiation for monetory calculations.
position_diff = df_hist['Position0'].diff()
df_hist['Position1'] = np.where(position_diff != 0.0, df_hist['Signal'], 0) 

df_hist['Position2'] = df_hist['Position1'] * df_hist['Close']

"""
Step Six: Filtering and Return Calculation
"""
df_ret = df_hist[df_hist['Position1'] != 0].copy()

df_ret.dropna(subset = ['Position2'], inplace = True)

df_ret['abs_returns'] = df_ret['Position2'].rolling(2).sum()
df_ret.loc[::2,'abs_returns'] = 0

#df_ret['abs_returns']=df_ret['abs_returns'].astype(float)
position2_shifted = df_ret['Position2'].shift(1)
df_ret['pct_returns'] = ((df_ret['abs_returns'] / position2_shifted) * 100).fillna(0)

df_ret['pct_returns_cumsum'] = df_ret['pct_returns'].cumsum()

"""
Step Seven: Save the Results
"""
df_ret.to_csv('aaa_returns.csv')
