
#import packages
import yfinance as yf
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
from IPython.display import display
pytrends = TrendReq()

#RETRIEVE DATA FROM YAHOO FINANCE
# List of tickers
tickers = ["BTC-USD", "SPY", "GLD", "DX-Y.NYB","^VIX"]

# Dictionary to store data
data = {}

# Download data for each ticker
for ticker in tickers:
  df = yf.download(ticker, 
  start='2017-7-3', 
  end='2022-9-19')
  data[ticker] = df

# Calculate the weekly return for each ticker in percentage
weekly_returns = {}
for ticker, df in data.items():
  weekly_returns[ticker] = df['Close'].pct_change(periods=7).resample('W').mean()*100

# Create a data frame with a multi-level index
df = pd.concat(weekly_returns, axis=1)
df.columns = pd.MultiIndex.from_product([tickers, ['Wk_return(%)']])
df.reset_index(inplace=True, drop=False)

#CALCULATE COVARIANCES
# Calculate the rolling covariance between bitcoin and each ticker
covariances = {}
for ticker in tickers[1:]:
    covariances[ticker] = df[tickers[0]]['Wk_return(%)'].rolling(12).cov(df[ticker]['Wk_return(%)'])

# Add the rolling covariances to the df data frame
for ticker, cov in covariances.items():
  df[ticker, 'Covariance'] = cov

df.drop(columns=[('^VIX', 'Covariance'), ('^VIX','Wk_return(%)')], inplace=True)


#INDEPENDENT VARIABLES
#Weekly average of VIX
df = df.assign(Avg_VIX=data['^VIX']['Close'].resample('W').mean())

#Covid
df['time_dummy'] = np.where((df['Date'] >= '2020-01-01') & (df['Date'] <= '2020-08-31'), 1, 0)
print(df)

'''
### bitcoin garch
###Google trends

# Read the column "A" from sheet "Sheet1" of the Excel file "file.xlsx"
excel_data = pd.read_excel("/Users/quanghuy/Desktop/Econpaper_file/Nguyen_Huy_Data.xlsx", sheet_name= "unclean", usecols= ["time","gg_trend_wrld"], dtype={'gg_trend_wrld': 'float'})
# Join excel data to df
#df_new = df.join(excel_data)
df_new = pd.merge(df, excel_data, left_index=True, right_index=True)

#print(df_new)
#df_new.to_csv('df.csv', index=True)
'''