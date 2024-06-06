import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
# Download historical stock price data
df = yf.download("HUBS", start="2024-03-11", end="2024-12-31", interval='1D')
print (df)

ticker = yf.Ticker('AAPL')
all_dates = ticker.quarterly_financials.columns
date = all_dates[0] 
total_shares = ticker.quarterly_financials.loc['Basic Average Shares', date]


stock_price = ticker.history(start='date', end='date')
if not stock_price.empty:
    closing_price = stock_price['Close'][0]
    market_cap = closing_price * total_shares
    print(f"Market Capitalization on {date}: {market_cap}")
else:
    print(f"No stock price data available for the date {date}")


# ZYebyBIQG_Rmc4KZBPZ64SN0gOo1ylju